import React, { useEffect, useState } from "react";
import withStyles from "@material-ui/core/styles/withStyles";
import { useHistory } from "react-router-dom";
import HomeIcon from "@material-ui/icons/Home";
import SearchIcon from "@material-ui/icons/Search";
import AccountCircleIcon from "@material-ui/icons/AccountCircle";
import "../nav.css";
import {
  Toolbar,
  AppBar,
  CssBaseline,
  LinearProgress,
} from "@material-ui/core";
import axios from "axios";
import Plot from "react-plotly.js";

const styles = (theme) => ({
  root: { margin: "100px" },
});

const back_end_uri = "http://127.0.0.1:5000/";

const Pair = (props) => {
  const { classes } = props;
  let history = useHistory();
  const [plot, setPlot] = useState({});
  const [uiLoading, setuiLoading] = useState(true);

  useEffect(() => {
    axios({
      method: "GET",
      url: `${back_end_uri}pair`,
    }).then((res) => {
      console.log(res.data);
      setPlot(res.data.fig);
      setuiLoading(false);
    });
  }, []);

  if (uiLoading) {
    return (
      <div className={classes.loading}>
        <LinearProgress />
      </div>
    );
  } else {
    return (
      <div>
        <CssBaseline />
        HELOOOOOOOO
        <Plot data={plot.data} layout={plot.layout} />
      </div>
    );
  }
};

export default withStyles(styles)(Pair);
