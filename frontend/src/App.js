import React, {Component} from 'react';
import PropTypes from 'prop-types';
import AppBar from 'material-ui/AppBar';
import './App.css';
import {MuiThemeProvider, createMuiTheme} from 'material-ui/styles';
import {withStyles} from 'material-ui/styles';
import Toolbar from 'material-ui/Toolbar';
import Typography from 'material-ui/Typography';
import Chart from './components/HorizontalStackedBarChart';
import axios from 'axios';

import Grid from 'material-ui/Grid';

const theme = createMuiTheme({
  palette: {
    primary: {
      light: '#b4ffff',
      main: '#80deea',
      dark: '#4bacb8',
      contrastText: '#000000',
    },
    secondary: {
      light: '#fa5788',
      main: '#c2185b',
      dark: '#8c0032',
      contrastText: '#ffffff',
    },
  },
});

const styles = {
  root: {
    flexGrow: 1,
  },
};

class App extends Component {
  state = {
    nps_data: [],
    client_data_2018: [],
    client_data_2017: [],
    client_data_2016: [],
    product_data_dna: [],

  };

  componentWillMount() {
    axios.get('/survey')
      .then(res => {
        console.log(res);
        this.setState({nps_data: res.data});
      });

    axios.get('/client_data?survey=February%202018%20NPS%20Survey')
      .then(res => {
        console.log(res);
        this.setState({client_data_2018: res.data});
      });
    axios.get('/client_data?survey=November%202017%20NPS%20Survey')
      .then(res => {
        console.log(res);
        this.setState({client_data_2017: res.data});
      });
    axios.get('/client_data?survey=Test%20Survey')
      .then(res => {
        console.log(res);
        this.setState({client_data_2016: res.data});
      });
    axios.get('/product_data?product=dna')
      .then(res => {
        console.log(res.data)
        this.setState({product_data_dna: res.data})
      });

  }

  render() {
    const {classes} = this.props;
    return (
      <MuiThemeProvider theme={theme}>
        <div className={classes.root}>
          <AppBar position="static" color="default">
            <Toolbar>
              <Typography variant="title" color="inherit">
                NPS Dashboard
              </Typography>
            </Toolbar>
          </AppBar>
        </div>

        <div>
          <Grid container>
            <Grid item>
              <Chart nps_data={this.state.product_data_dna} width={800} height={400}/>
            </Grid>
          </Grid>
        </div>
      </MuiThemeProvider>
    );
  }
}


App.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles, {withTheme: true})(App);
