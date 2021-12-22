import React, { useEffect, useState } from "react";
import withStyles from "@material-ui/core/styles/withStyles";
import { useHistory, useLocation } from "react-router-dom";
import HomeIcon from "@material-ui/icons/Home";
import SearchIcon from "@material-ui/icons/Search";
import AccountCircleIcon from "@material-ui/icons/AccountCircle";
import Nav from "../components/navigation";
import { DataGrid, GridToolbar } from "@material-ui/data-grid";
import {
  Toolbar,
  Typography,
  AppBar,
  Box,
  CssBaseline,
  LinearProgress,
} from "@material-ui/core";
import axios from "axios";
import "../pair.css";
import Plot from "react-plotly.js";
import Loading from "../components/loading";

const styles = (theme) => ({
  main: { marginTop: "100px" },
  plotContainer: { width: "100%" },
  title: {
    marginLeft: "420px",
    marginBottom: "20px",
  },
});

const back_end_uri = "http://127.0.0.1:5000/";
// const back_end_uri = "https://c75d890655a7.ngrok.io/";

const Pair = (props) => {
  const { classes } = props;
  let history = useHistory();
  let location = useLocation();
  let state = location.state;
  const [plot, setPlot] = useState({});
  const [newsPlot, setNewsPlot] = useState({});
  const [twitterPlot, setTwitterPlot] = useState({});
  const [newsAvgPlot, setNewsAvgPlot] = useState({});
  const [twitterAvgPlot, setTwitterAvgPlot] = useState({});
  const [twitterVolPlot, setTwitterVolPlot] = useState({});
  const [uiLoading, setuiLoading] = useState(true);
  const [tableRows, setTableRows] = useState([]);
  const [tableColumns, setTableColumns] = useState([]);
  const [prediction, setPrediction] = useState([]);
  const [defaultLayout, setDefaultLayout] = useState({
    template: "plotly_dark",
    paper_bgcolor: "#2d353d",
    plot_bgcolor: "#2d353d",
    margin_l: 40,
    margin_r: 40,
    margin_b: 40,
    margin_t: 50,
    font_family: "Montserrat",
  });

  const changeFormat = (params, key) => {
    let color = "";
    let formatted;
    if (["Close", "Open", "High", "Low", "Volume"].includes(key)) {
      formatted = "$" + params.value.replace(/\d(?=(\d{3})+\.)/g, "$&,");
    } else {
      if (["Change"].includes(key)) {
        let num = Number(params.value);
        formatted = `${num /** 100*/
          .toLocaleString()} %`;
      }
    }
    if (["Change", "Close"].includes(key)) {
      if (Number(params.row["Close"]) > Number(params.row["Open"])) {
        formatted += " ↗";
        color = "green";
      } else {
        if (Number(params.row["Close"]) < Number(params.row["Open"])) {
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
      url: `${back_end_uri}pair?pair=${state.pair}`,
    }).then((res) => {
      console.log(res.data.price);
      let tableRows = res.data.price;
      let tableColumns = [];
      // res.data.price.forEach((row) => {
      //   tableRows.push(row);
      // });
      // tableRows.push(row);
      Object.keys(res.data.price[0]).forEach((key) => {
        console.log(key);
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
            if (["Close", "Open", "High", "Low", "Volume"].includes(key)) {
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
      setPlot(res.data.fig);
      setNewsPlot(res.data.newsPlot);
      setTwitterPlot(res.data.twitterPlot);
      setNewsAvgPlot(res.data.newsAvgPlot);
      setTwitterAvgPlot(res.data.twitterAvgPlot);
      setTwitterVolPlot(res.data.twitterVolPlot);
      setPrediction(res.data.prediction);
      setTableRows(tableRows);
      setTableColumns(tableColumns);
      setuiLoading(false);
    });
  }, []);

  if (uiLoading) {
    return <Loading />;
  } else {
    return (
      <div className={classes.main}>
        <AppBar position="fixed" className={classes.bar} color="secondary">
          <Nav />
        </AppBar>
        <CssBaseline />
        <div className={classes.title}>
          <Typography variant="h4">
            Coin Pair: {tableRows[0]["Coin Pair"]}
          </Typography>
        </div>
        <div className={classes.plotContainer}>
          <center>
            <Plot data={plot.data} layout={plot.layout} />
          </center>
        </div>
        <div style={{ marginTop: "10px" }} className={classes.title}>
          <Typography variant="h4">Price Chart</Typography>
        </div>
        <center>
          <Box style={{ height: 400, width: "60%" }}>
            <DataGrid
              components={{
                Toolbar: GridToolbar,
              }}
              borderColor="primary.dark"
              density="standard"
              hideFooter={true}
              rows={tableRows}
              columns={tableColumns}
            />
          </Box>
        </center>
        <div style={{ marginTop: "10px" }} className={classes.title}>
          <Typography variant="h4">Prediction Chart</Typography>
        </div>
        <center>
          <Box style={{ height: 400, width: "60%" }}>
            {console.log(prediction)}
            <DataGrid
              components={{
                Toolbar: GridToolbar,
              }}
              borderColor="primary.dark"
              density="standard"
              hideFooter={true}
              rows={prediction}
              columns={[
                {
                  field: "2",
                  headerName: "Predicted Price",
                  align: "center",
                  editable: false,
                  flex: 0.5,
                  renderCell: (params) => {
                    return (
                      "$" +
                      ("" + params.value).replace(/\d(?=(\d{3})+\.)/g, "$&,")
                    );
                  },
                },
                {
                  field: "Date",
                  headerName: "Date",
                  align: "center",
                  editable: false,
                  flex: 0.5,
                },
              ]}
            />
          </Box>
        </center>
        <center>
          <table>
            <tbody>
              <tr>
                <center>
                  <td>
                    <div style={{ marginBottom: "20px", marginTop: "10px" }}>
                      <Typography variant="h4">
                        Historical News Sentiment
                      </Typography>
                    </div>
                    <Plot data={newsPlot.data} layout={newsPlot.layout} />
                  </td>
                  <td>
                    <div style={{ marginBottom: "20px", marginTop: "10px" }}>
                      <Typography variant="h4">
                        Average News Sentiment
                      </Typography>
                    </div>
                    <Plot
                      data={newsAvgPlot ? newsAvgPlot.data : {}}
                      layout={newsAvgPlot ? newsAvgPlot.layout : defaultLayout}
                    />
                  </td>
                </center>
              </tr>
              <tr>
                <center>
                  <td>
                    <div style={{ marginBottom: "20px", marginTop: "10px" }}>
                      <Typography variant="h4">
                        Twitter News Volume and Sentiment by Day
                      </Typography>
                    </div>
                    <Plot
                      data={twitterPlot ? twitterPlot.data : {}}
                      layout={twitterPlot ? twitterPlot.layout : defaultLayout}
                    />
                  </td>
                  <td>
                    <div style={{ marginBottom: "20px", marginTop: "10px" }}>
                      <Typography variant="h4">
                        Average Twitter Sentiment
                      </Typography>
                    </div>
                    <Plot
                      data={twitterAvgPlot ? twitterAvgPlot.data : {}}
                      layout={
                        twitterAvgPlot ? twitterAvgPlot.layout : defaultLayout
                      }
                    />
                  </td>
                </center>
              </tr>
              <tr>
                <center>
                  <td>
                    <div style={{ marginBottom: "20px", marginTop: "10px" }}>
                      <Typography variant="h4">
                        Volume of Twitter Posts in Last Two Weeks by Sentiment
                      </Typography>
                    </div>
                    <Plot
                      data={twitterVolPlot ? twitterVolPlot.data : {}}
                      layout={
                        twitterVolPlot ? twitterVolPlot.layout : defaultLayout
                      }
                    />
                  </td>
                </center>
              </tr>
            </tbody>
          </table>
        </center>
      </div>
    );
  }
};

export default withStyles(styles)(Pair);

// C:\Users\denni\AppData\Local\Programs\Python\Python38\Scripts>
