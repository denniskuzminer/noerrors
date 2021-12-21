import React from "react";
import withStyles from "@material-ui/core/styles/withStyles";

import { LinearProgress, Typography } from "@material-ui/core";

import "../landing.css";

const styles = (theme) => ({
  loading: {
    backgroundColor: theme.palette.background.default,
    height: "100vh",
    width: "100%",
    position: "absolute",
  },
  loadingContainer: {
    position: "absolute",
    left: 600,
    right: 600,
    top: "40%",
  },
});

const Loading = (props) => {
  const { classes } = props;
  return (
    <div className={classes.loading}>
      <center className={classes.loadingContainer}>
        <table>
          <tbody>
            <tr>
              <td>
                <div className="move"></div>
              </td>
              <td>
                <div className="move"></div>
              </td>
              <td>
                <div className="move"></div>
              </td>
              <td>
                <Typography
                  variant="h3"
                  style={{ color: "rgb(175, 175, 175)" }}
                >
                  Loading Crypto Data
                </Typography>
              </td>
              <td>
                <div className="move"></div>
              </td>
              <td>
                <div className="move"></div>
              </td>
              <td>
                <div className="move"></div>
              </td>
            </tr>
          </tbody>
        </table>
        <br />
        <LinearProgress style={{ color: "rgb(175, 175, 175)" }} />
      </center>
    </div>
  );
};
export default withStyles(styles)(Loading);
