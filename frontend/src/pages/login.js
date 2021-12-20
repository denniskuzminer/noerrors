import React, { useEffect, useState } from "react";
import withStyles from "@material-ui/core/styles/withStyles";
import { useHistory } from "react-router-dom";
import Nav from "../components/navigation";
import {
  AppBar,
  CssBaseline,
  TextField,
  Button,
  Grid,
  Link,
  Container,
  Avatar,
  Typography,
  LinearProgress,
  Box,
  CircularProgress,
} from "@material-ui/core";
import LockOutlinedIcon from "@material-ui/icons/LockOutlined";
import AccountCircleIcon from "@material-ui/icons/AccountCircle";
import LockIcon from "@material-ui/icons/Lock";
import EmailIcon from "@material-ui/icons/Email";
import axios from "axios";

const styles = (theme) => ({
  root: { margin: "100px" },
  paper: {
    marginTop: "100px",
  },
  header: {
    // justifyContent: "center",
    // border: "5px solid black",
  },
  register: { cursor: "pointer", marginLeft: "10px" },
  login: { cursor: "pointer" },
  chosen: { textDecoration: "underline" },
});

const back_end_uri = "http://127.0.0.1:5000/";

const Login = (props) => {
  const { classes } = props;
  let history = useHistory();
  const [uiLoading, setuiLoading] = useState(true);
  const [register, setRegister] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [errors, setErrors] = useState("");

  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    axios({
      method: "POST",
      url: `${back_end_uri}login`,
      headers: { "Access-Control-Allow-Origin": "*" },
      data: {
        username: username,
        password: password,
        email: email,
        register: email === "" ? "False" : "True",
      },
    })
      .then((res) => {
        setErrors("");
        history.push({
          pathname: "/",
        });
      })
      .catch((error) => {
        console.log(error.response);
        if (error.response.status == 403) {
          if (error.response.data.includes("username or password incorrect")) {
            setErrors("The username or password you entered is incorrect.");
          } else {
            setErrors(
              "This username is already taken. Please use another username."
            );
          }
        }
      });
  };

  const handleRegister = () => {
    setRegister(true);
  };

  const handleLogin = () => {
    setRegister(false);
  };

  useEffect(() => {
    setuiLoading(false);
  }, []);

  if (uiLoading) {
    return (
      <div className={classes.loading}>
        <LinearProgress />
      </div>
    );
  } else {
    return (
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <AppBar position="fixed" className={classes.bar} color="secondary">
          <Nav />
        </AppBar>
        <CssBaseline />
        <div className={classes.paper}>
          <div className={classes.header}>
            <table>
              <tbody>
                <td
                  onClick={handleLogin}
                  className={`${classes.login}${
                    register ? "" : " " + classes.chosen
                  }`}
                >
                  <Typography component="h1" variant="h5">
                    Login
                  </Typography>
                </td>
                <td
                  onClick={handleRegister}
                  className={`${classes.register}${
                    register ? " " + classes.chosen : ""
                  }`}
                >
                  <Typography component="h1" variant="h5">
                    Register
                  </Typography>
                </td>
              </tbody>
            </table>
          </div>
          <form className={classes.form} onSubmit={handleSubmit} noValidate>
            <Box sx={{ display: "flex", alignItems: "center" }}>
              <AccountCircleIcon
                sx={{ color: "action.active", mr: 1, my: 0.5 }}
              />
              <TextField
                variant="outlined"
                margin="normal"
                required
                fullWidth
                name="username"
                label="Username"
                type="username"
                id="username"
                autoFocus
                onChange={handleUsernameChange}
              />
            </Box>
            <Box sx={{ display: "flex", alignItems: "center" }}>
              <LockIcon sx={{ color: "action.active", mr: 1, my: 0.5 }} />
              <TextField
                variant="outlined"
                margin="normal"
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password"
                autoComplete="current-password"
                onChange={handlePasswordChange}
              />
            </Box>
            {register && (
              <Box sx={{ display: "flex", alignItems: "center" }}>
                <EmailIcon sx={{ color: "action.active", mr: 1, my: 0.5 }} />
                <TextField
                  variant="outlined"
                  margin="normal"
                  required
                  fullWidth
                  id="email"
                  label="Email Address"
                  name="email"
                  autoComplete="email"
                  onChange={handleEmailChange}
                />
              </Box>
            )}
            {errors !== "" && (
              <div>
                <Typography>{errors}</Typography>
              </div>
            )}
            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="secondary"
              className={classes.submit}
            >
              {register ? "Register" : "Sign In"}
            </Button>
          </form>
        </div>
      </Container>
    );
  }
};

export default withStyles(styles)(Login);
