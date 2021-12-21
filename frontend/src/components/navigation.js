import React, { useEffect, useState } from "react";
import withStyles from "@material-ui/core/styles/withStyles";
import { useHistory } from "react-router-dom";
import HomeIcon from "@material-ui/icons/Home";
import SearchIcon from "@material-ui/icons/Search";
import AccountCircleIcon from "@material-ui/icons/AccountCircle";
import "../nav.css";
import { Toolbar, AppBar, CssBaseline, Box } from "@material-ui/core";
import axios from "axios";

const styles = (theme) => ({
  root: { margin: "100px" },
});

const back_end_uri = "http://127.0.0.1:5000/";

const Nav = (props) => {
  const { classes } = props;
  let history = useHistory();
  const [showSearch, setShowSearch] = [props.showSearch, props.setShowSearch];
  const [binanceData, setBinanceData] = [
    props.binanceData,
    props.setBinanceData,
  ];

  const handleShowSearch = (event) => {
    event.preventDefault();
    setShowSearch(!showSearch);
  };

  const handleLogout = () => {
    if (binanceData.username !== "") {
      axios({
        method: "PUT",
        url: `${back_end_uri}logout`,
      }).then((res) => {
        console.log(res.data);
        setBinanceData(res.data);
      });
      return history.push({
        pathname: `/`,
      });
    }
    return history.push({
      pathname: `/login`,
    });
  };

  return (
    <Toolbar style={{ justifyContent: "right" }}>
      <CssBaseline />
      <nav>
        <table style={{ marginTop: "-15px" }}>
          <tbody>
            <tr>
              <td></td>
              <td>
                <ul>
                  <li>
                    <HomeIcon />
                    <a style={{ marginTop: "-10px" }} href="./">
                      Home
                    </a>
                  </li>
                  <li>
                    <SearchIcon />
                    <a href="" onClick={handleShowSearch}>
                      Search
                    </a>
                  </li>
                  <li>
                    <AccountCircleIcon />
                    <a onClick={handleLogout}>
                      {binanceData === undefined || binanceData.username === ""
                        ? "Login"
                        : `Logout of ${binanceData.username}`}
                      {/* {console.log(binanceData)} */}
                    </a>
                  </li>
                </ul>
              </td>
            </tr>
          </tbody>
        </table>
      </nav>
    </Toolbar>
  );
};

export default withStyles(styles)(Nav);
