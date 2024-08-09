using Microsoft.AspNetCore.Mvc;
using TMDbLib.Client;
using TMDbLib.Objects.General;
using TMDbLib.Objects.Search;

namespace uncas.dk.Controllers;

[ApiController]
[Route("[controller]")]
public class MovieWatchProvidersController : ControllerBase
{
    private readonly ILogger<MovieWatchProvidersController> _logger;
    private readonly IConfiguration _config;

    public MovieWatchProvidersController(
        ILogger<MovieWatchProvidersController> logger,
        [FromServices] IConfiguration config)
    {
        _logger = logger;
        _config = config;
    }

    [HttpGet]
    public async Task<MovieWatchProvidersResponse> Get([FromQuery] string movie)
    {
        var client = new TMDbClient(_config.GetSection("TheMovieDB").GetValue<string>("ApiKey"));
        SearchContainer<SearchMovie> results = await client.SearchMovieAsync(movie);
        if (results.Results.Count == 0)
        {
            return MovieWatchProvidersResponse.Empty;
        }

        var foundMovie = results.Results[0];
        var movieId = foundMovie.Id;

        Dictionary<string, WatchProviders> watchProviders = (await client.GetMovieWatchProvidersAsync(movieId)).Results;

        var myCountry = "DK";
        if (!watchProviders.TryGetValue(myCountry, out WatchProviders? myCountryProviders))
        {
            return MovieWatchProvidersResponse.Empty;
        }

    	var	myProviders = new string[]{"Viaplay", "HBO Max", "Netflix", "TV 2 Play"};

        var ads = myCountryProviders.Ads?? new List<WatchProviderItem>();
        var flatrate = myCountryProviders.FlatRate?? new List<WatchProviderItem>();
        var providers = ads.Union(flatrate);

        List<string> onMyProviders =providers.Select(provider=>provider.ProviderName).Where(provider=>myProviders.Contains(provider)).ToList();

        return new MovieWatchProvidersResponse
        {
            Movie = foundMovie.Title,
            WatchProviders = onMyProviders
        };
    }
}

public class MovieWatchProvidersResponse
{
    public required string Movie { get; set; }
    public required IEnumerable<string> WatchProviders { get; set; }

    public static MovieWatchProvidersResponse Empty => new MovieWatchProvidersResponse
    {
        Movie = string.Empty,
        WatchProviders = Array.Empty<string>()
    };
}