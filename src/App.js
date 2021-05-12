import React from "react";
import Pokedex from "./compo/Pokedex";
import Pokemon from "./compo/Pokemon";
import Master from "./compo/Master";
import { Route, Switch } from "react-router-dom";

const App = () => (
  <Switch>
    <Route exact path="/" render={(props) => <Master {...props} />} />
    <Route
      exact
      path="/:pokemonId"
      render={(props) => <Pokemon {...props} />}
    />
  </Switch>
);

export default App;