import React, { useEffect, useState } from "react";
import withStyles from "@material-ui/core/styles/withStyles";
import { useHistory } from "react-router-dom";
import axios from "axios";
import { DataGrid, GridToolbar } from "@material-ui/data-grid";
import PropTypes from "prop-types";
import { borders } from "@material-ui/system";
import InputBase from "@material-ui/core/InputBase";
import SearchIcon from "@material-ui/icons/Search";
import Tooltip from "@material-ui/core/Tooltip";
import AddIcon from "@material-ui/icons/Add";
import {
  LinearProgress,
  List,
  ListItem,
  ListItemIcon,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Slide,
  ListItemText,
  Toolbar,
  CssBaseline,
  Drawer,
  InputAdornment,
  Typography,
  AppBar,
  Slider,
  Divider,
  Select,
  MenuItem,
  Input,
  TextField,
  Box,
  Button,
  Card,
  CardContent,
} from "@material-ui/core";
import Plot from "react-plotly.js";
import MonetizationOnOutlinedIcon from "@material-ui/icons/MonetizationOnOutlined";
import "../landing.css";
import Nav from "../components/navigation";
import Loading from "../components/loading";

const back_end_uri = "http://127.0.0.1:5000/";
// const back_end_uri = "https://c75d890655a7.ngrok.io/";

const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});

const styles = (theme) => ({
  root: {
    margin: "100px 200px 100px 200px",
    // marginLeft: "380px",
    overFlowX: "hidden",
  },
  heading: {
    // margin: "100px",
    margin: "100px 200px 100px 200px",
    marginBottom: "-80px",
    // width: "100%",
    height: "130px",
    borderTop: "1px solid #8a8a8a",
    borderBottom: "1px solid #8a8a8a",
  },
  headingContents: {
    marginTop: "30px",
    // marginLeft: "285px",
  },
  loading: {
    backgroundColor: theme.palette.background.default,
    height: "100vh",
    width: "100%",
    position: "absolute",
  },
  title: { marginBottom: "20px" },
  loadingContainer: {
    position: "absolute",
    left: 600,
    right: 600,
    top: "40%",
  },
  searchBox: {
    // background: theme.palette.background.default,
    width: "900px",
    backgroundColor: theme.palette.background.default,
    height: "600px",
    overflowY: "scroll",
    overflowX: "hidden",
  },
  container: {
    backgroundColor: theme.palette.background.default,
    color: theme.palette.primary.contrastText,
  },
  datagrid: {
    backgroundColor: theme.palette.background.contrast,
  },
  bar: {
    zIndex: theme.zIndex.drawer + 1,
  },
  drawer: {
    background: theme.palette.background.default,
  },
  drawerContents: {
    // border: "5px solid yellow",
    // height: "100vh",
    height: "100%",
    background: theme.palette.background.default,
    marginTop: "58px",
  },
  grid: {
    width: "calc(100%)",
    marginTop: "30px",
  },
  main: {
    overflowX: "hidden",
    backgroundColor: theme.palette.background.default,
  },
  slider: {
    /* border: "5px solid black"*/
  },
  search: {
    position: "relative",
    border: "1px solid #8a8a8a",
    borderRadius: "10px",
    marginLeft: 0,
    width: "100%",
    [theme.breakpoints.up("sm")]: {
      marginLeft: theme.spacing(1),
      width: "auto",
    },
    justifyContent: "right",
  },
  searchResult: {
    backgroundColor: theme.palette.background.default,
    height: "60px",
    cursor: "pointer",
    borderTop: "1px solid #8a8a8a",
    borderBottom: "1px solid #8a8a8a",
    // width: "97%",
    marginLeft: "10px",
    "&:hover": {
      background: "#8a8a8a",
    },
  },
  searchIcon: {
    padding: theme.spacing(0, 2),
    height: "100%",
    position: "absolute",
    pointerEvents: "none",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
  inputRoot: {
    color: "inherit",
  },
  searchResultContainer: {
    alignItems: "center",
    justifyContent: "center",
  },
  inputInput: {
    padding: theme.spacing(1, 1, 1, 0),
    // vertical padding + font size from searchIcon
    paddingLeft: `calc(1em + ${theme.spacing(4)}px)`,
    transition: theme.transitions.create("width"),
    width: "100%",
    [theme.breakpoints.up("sm")]: {
      width: "12ch",
      "&:focus": {
        width: "20ch",
      },
    },
  },
});
function ValueLabelComponent(props) {
  const { children, open, value } = props;

  return (
    <Tooltip open={open} enterTouchDelay={0} placement="top" title={value}>
      {children}
    </Tooltip>
  );
}

ValueLabelComponent.propTypes = {
  children: PropTypes.element.isRequired,
  open: PropTypes.bool.isRequired,
  value: PropTypes.number.isRequired,
};

const Landing = (props) => {
  const { classes } = props;
  const [binanceData, setBinanceData] = useState({});
  const [tableRows, setTableRows] = useState([]);
  const [tableColumns, setTableColumns] = useState([]);
  const [value, setValue] = useState(10);
  const [showSearch, setShowSearch] = useState(false);
  const [orderBy, setOrderBy] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [CMCVol, setCMCVol] = useState({});
  const [CMCActive, setCMCActive] = useState({});
  const [searchResults, setSearchResults] = useState([]);
  const [uiLoading, setuiLoading] = useState(true);
  let history = useHistory();

  const changeFormat = (params, key) => {
    let color = "";
    let formatted;
    if (["Close", "Open", "Volume"].includes(key)) {
      formatted =
        "$" + params.value.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, "$&,");
    } else {
      if (["Change"].includes(key)) {
        let num = Number(params.value);
        formatted = `${num /** 100*/
          .toLocaleString()} %`;
      }
    }
    if (["Change", "Close"].includes(key)) {
      if (Number(params.row["Change"]) > 0) {
        formatted += " ↗";
        color = "green";
      } else {
        if (Number(params.row["Change"]) < 0) {
          formatted += " ↘";
          color = "red";
        } else {
          formatted += " ";
          color = "white";
        }
      }
    }
    return (
      <span>
        <span style={{ color: color }}>{formatted}</span>
      </span>
    );
  };

  const changeFormatSearch = (row, key) => {
    let params = { value: row[key], row: row };
    return changeFormat(params, key);
  };

  useEffect(() => {
    axios({
      method: "GET",
      url: back_end_uri,
      headers: { "Access-Control-Allow-Origin": "*" },
    }).then((res) => {
      let tableRows = [];
      let tableColumns = [];
      setBinanceData(res.data);
      res.data.binanceData.forEach((tableList, idx) => {
        tableRows.push(tableList);
        if (tableList.length !== 0) {
          Object.keys(tableList[0]).forEach((key) => {
            if (!["id", "AbsChange"].includes(key)) {
              if (["Change"].includes(key)) {
                tableColumns.push({
                  field: key,
                  headerName: key,
                  align: "center",
                  editable: false,
                  flex: 0.5,
                  renderCell: (params) => {
                    return changeFormat(params, key);
                  },
                });
              } else {
                if (["Close", "Open", "Volume"].includes(key)) {
                  tableColumns.push({
                    field: key,
                    headerName: key,
                    align: "center",
                    editable: false,
                    flex: 0.5,
                    renderCell: (params) => {
                      return changeFormat(params, key);
                    },
                  });
                } else {
                  tableColumns.push({
                    field: key,
                    headerName: key,
                    align: "left",
                    editable: false,
                    flex: 0.5,
                  });
                }
              }
            }
          });
        }
      });
      setTableRows(tableRows);
      setTableColumns(tableColumns);
      setCMCVol(res.data.CMCVol);
      setCMCActive(res.data.CMCActive);
      setuiLoading(false);
    });
  }, []);

  const handleNumberRecordsChange = (event, newValue) => {
    setValue(newValue);
    console.log(tableRows);
  };

  const handleRowClick = (event) => {
    console.log(event);
    history.push({
      pathname: `/pair?pair=${event.row["Coin Pair"]}`,
      state: { pair: event.row["Coin Pair"] },
    });
  };

  const handleInputChange = (event) => {
    setValue(event.target.value === "" ? "" : Number(event.target.value));
  };

  const handleAdd = async (event, pair) => {
    event.stopPropagation();
    console.log(pair);
    await axios({
      method: "POST",
      url: `${back_end_uri}add?pair=${pair["Coin Pair"]}`,
    }).then((res) => {
      let tableRowsTemp = tableRows.map((item) =>
        Object.assign([], item, { selected: false })
      );
      let temp = tableRowsTemp[0];
      temp.push(pair);
      tableRowsTemp[0] = temp;
      setTableRows(tableRowsTemp);
    });
  };

  const handleShowSearch = () => {
    setShowSearch(!showSearch);
  };

  const handleSearchClick = (event) => {
    let pair = event.currentTarget.getAttribute("pair");
    history.push({
      pathname: `/pair?pair=${pair}`,
      state: { pair: pair },
    });
  };

  const handleSearch = (event) => {
    setSearchQuery(event.target.value);
    if (event.target.value === "") {
      setSearchResults([]);
    } else {
      let filtered = binanceData.binanceData[1].filter((row) =>
        row["Coin Pair"].includes(event.target.value.toUpperCase())
      );
      console.log(filtered);
      setSearchResults(filtered);
    }
  };

  if (uiLoading) {
    return <Loading />;
  } else {
    return (
      <div className={classes.main}>
        <CssBaseline />
        <AppBar position="fixed" className={classes.bar} color="secondary">
          <Nav
            binanceData={binanceData}
            setBinanceData={setBinanceData}
            showSearch={showSearch}
            setShowSearch={setShowSearch}
          />
        </AppBar>
        {/* <Drawer
          style={{ backgroundColor: "#1C1C1C !important" }}
          className={classes.drawer}
          variant="permanent"
          anchor="left"
        >
          <List className={classes.drawerContents}>
            <ListItem>
              <Box sx={{ display: "flex", alignItems: "flex-end" }}>
                <MonetizationOnOutlinedIcon
                  color="secondary"
                  sx={{ color: "action.active", mr: 1, my: 0.5 }}
                />
                <TextField
                  size="small"
                  label="Quote Currency"
                  variant="outlined"
                  defaultValue="USDT"
                  color="secondary"
                />
              </Box>
              <Button color="secondary">Change</Button>
            </ListItem>
            <ListItem>
              <Typography color="secondary">Max Items Displayed</Typography>
              <Slider
                className={classes.slider}
                value={value}
                ValueLabelComponent={ValueLabelComponent}
                min={1}
                max={350}
                color="secondary"
                onChange={handleNumberRecordsChange}
              />
              <Input
                className={classes.input}
                value={value}
                margin="dense"
                color="secondary"
                onChange={handleInputChange}
                inputProps={{
                  step: 10,
                  min: 1,
                  max: 350,
                  type: "number",
                }}
              />
            </ListItem>
          </List>
        </Drawer> */}
        <Dialog
          open={showSearch}
          TransitionComponent={Transition}
          keepMounted
          maxWidth={"md"}
          onClose={handleShowSearch}
        >
          <div className={classes.searchBox}>
            <DialogTitle>{"Search"}</DialogTitle>
            <DialogContent>
              <div className={classes.search}>
                <div className={classes.searchIcon}>
                  <SearchIcon />
                </div>
                <InputBase
                  variant="outlined"
                  placeholder="Search..."
                  classes={{
                    root: classes.inputRoot,
                    input: classes.inputInput,
                  }}
                  onChange={handleSearch}
                  inputProps={{ "aria-label": "search" }}
                />
              </div>
              <div className={classes.searchResultContainer}>
                {searchResults.map((row, i) => (
                  <Card
                    onClick={handleSearchClick}
                    pair={row["Coin Pair"]}
                    className={classes.searchResult}
                    key={i}
                  >
                    <CardContent>
                      <table style={{ width: "100%" }}>
                        <tbody>
                          <tr>
                            <td>{row["Coin Pair"]}</td>
                            <td>{changeFormatSearch(row, "Change")}</td>
                            <td>{changeFormatSearch(row, "Close")}</td>
                            {binanceData["username"] !== "" && (
                              <td>
                                <AddIcon onClick={(e) => handleAdd(e, row)} />
                              </td>
                            )}
                          </tr>
                        </tbody>
                      </table>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </DialogContent>
          </div>
        </Dialog>

        <div className={classes.heading}>
          <div className={classes.headingContents}>
            <Typography variant="h3">
              Cryptocurrency Sentiment Analyzer
            </Typography>
          </div>
        </div>
        <div className={classes.root}>
          <div>
            <Typography variant="h4">
              {binanceData["username"] === "" ? "Currencies" : "Favorites"}
            </Typography>
            <Box style={{ height: 400, width: "100%" }}>
              <DataGrid
                className={classes.datagrid}
                components={{
                  Toolbar: GridToolbar,
                }}
                borderColor="primary.dark"
                density="standard"
                hideFooter={true}
                // rows={tableRows[1]}
                rows={binanceData["username"] ? tableRows[0] : tableRows[3]}
                columns={tableColumns}
                onRowClick={handleRowClick}
                components={{
                  NoRowsOverlay: () => (
                    <center style={{ marginTop: "200px" }}>
                      <Typography>
                        No favorites yet. Add new currencies to favorite with
                        the search bar.
                      </Typography>
                    </center>
                  ),
                }}
              />
            </Box>
            <table className={classes.grid}>
              <tbody>
                <tr>
                  <td>
                    <Typography variant="h4">Top Movers</Typography>
                    <Box style={{ height: 400, width: "100%" }}>
                      <DataGrid
                        className={classes.datagrid}
                        components={{
                          Toolbar: GridToolbar,
                        }}
                        borderColor="primary.dark"
                        density="standard"
                        hideFooter={true}
                        rows={tableRows[1]}
                        onRowClick={handleRowClick}
                        columns={tableColumns}
                        id="id"
                      />
                    </Box>
                  </td>
                  <td>
                    <Typography variant="h4">Top Priced</Typography>
                    <Box style={{ height: 400, width: "100%" }}>
                      <DataGrid
                        className={classes.datagrid}
                        components={{
                          Toolbar: GridToolbar,
                        }}
                        borderColor="primary.dark"
                        density="standard"
                        hideFooter={true}
                        onRowClick={handleRowClick}
                        rows={tableRows[2]}
                        columns={tableColumns}
                        id="id"
                      />
                    </Box>
                  </td>
                </tr>
                <tr>
                  <td>
                    <div
                      style={{ marginTop: "10px" }}
                      className={classes.title}
                    >
                      <Typography variant="h4">
                        Top 10 Cryptos by Market Cap
                      </Typography>
                    </div>
                    <center>
                      <Plot
                        data={CMCVol ? CMCVol.data : {}}
                        layout={CMCVol.layout}
                      />
                    </center>
                  </td>
                  <td>
                    <div
                      style={{ marginTop: "10px" }}
                      className={classes.title}
                    >
                      <Typography variant="h4">
                        Top 10 Most Active Cryptos in Last 24hrs
                      </Typography>
                    </div>
                    <center>
                      <Plot
                        data={CMCActive ? CMCActive.data : {}}
                        layout={CMCActive.layout}
                      />
                    </center>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    );
  }
};

export default withStyles(styles)(Landing);
