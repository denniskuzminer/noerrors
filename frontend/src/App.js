import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Landing from "./pages/landing";
import Login from "./pages/login";
import Pair from "./pages/pair";

const App = (props) => {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={Landing} />
        <Route exact path="/login" component={Login} />
        <Route path="/pair" component={Pair} />
      </Switch>
    </Router>
  );
};

export default App;
