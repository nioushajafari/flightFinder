import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props)
    this.state = { origins: [ 'NYC', 'BOS' ] }
  }
  addOriginClicked() {
    this.setState({ origins: this.state.origins.concat(['']) })
  }
  removeOriginClicked(i) {
    this.setState({ origins: this.state.origins.slice(0, i).concat(this.state.origins.slice(i+1, this.state.origins.length )) })
  }
  async searchClicked() {
    // let queryObj = {
    //   origins: this.state.origins,
    //   dates: this.state.dates
    // }
    const settings = {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(this.state)
    }
    let response = await fetch('http://localhost:5000/search', settings)
    let obj = await response.json()
    console.log(obj)
    this.setState({ flights: obj })
  }
  render() {
    return (
      <div>
        <h1>Meet me in the middle</h1>
        <h2>Where are people coming from?</h2>
        {
          this.state.origins.map((origin, i) =>
            <div key={i}>
              <input type='text' value={origin}></input>
              <input type='button' value='Remove' onClick={ (() => { this.removeOriginClicked(i) }).bind(this) }></input>
            </div>
          )
        }
        <input type='button' value='+' onClick={ this.addOriginClicked.bind(this) }></input>
        <h2>What dates do you want to meet?</h2>
        <p> Arrival: <input type='date'></input></p>
        <p> Departure: <input type='date'></input></p>
        <input type='button' value='Search' onClick={ this.searchClicked.bind(this) }></input>
        <h1>Search results</h1>
        { JSON.stringify(this.state.flights) }
      </div>
    );
  }
}

export default App;
