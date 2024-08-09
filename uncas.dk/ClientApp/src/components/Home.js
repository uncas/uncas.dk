import React, { Component } from 'react';

export class Home extends Component {
  static displayName = Home.name;

  render() {
    const projects = [
      {
        name: "Blog at olelynge.com",
        url: "https://olelynge.com"
      },
      {
        name: "Repositories",
        url: "https://github.com/uncas"
      },
      {
        name: "Fri Læring Med Leg",
        url: "https://learnplay.azurewebsites.net/"
      }
    ]
    return (
      <div className="App">
        <header className="App-header">
          <h2>
            Welcome to uncas.dk
          </h2>
          {projects.map(project => (
            <div>
              <a
                className="App-link"
                href={project.url}
                target="_blank"
                rel="noopener noreferrer"
              >
                {project.name}
              </a>
            </div>
          ))}
        </header>
      </div>
    );
  }
}