import { createMuiTheme } from "@material-ui/core/styles";

const theme = createMuiTheme({
  components: {
    background: {
      // default: "#212121",
    },
  },
  background: {
    contrast: "#2d353d",
    default: "#1e2933",
    // default: "#fff",
  },
  palette: {
    background: {
      contrast: "#2d353d",
      default: "#1e2933",
      // default: "#fff",
    },
    borderColor: {
      main: "#131C23",
    },
    primary: {
      light: "#9e5a63",
      main: "#a5a7aa",
      dark: "#314455",
      contrastText: "#fff",
    },
    secondary: {
      light: "#ff7476",
      main: "#14FFEC",
      dark: "#bd0022",
      contrastText: "#fff",
    },
    text: {
      primary: "#CBCED3",
    },
  },

  typography: {
    fontFamily: ["Montserrat", "regular"].join(","),
  },
});

export default theme;
