import React, {Component} from 'react';
import PropTypes from 'prop-types';
import AppBar from 'material-ui/AppBar';
import {connect} from 'react-redux';
import './App.css';
import {MuiThemeProvider, createMuiTheme} from 'material-ui/styles';
import {withStyles} from 'material-ui/styles';
import Toolbar from 'material-ui/Toolbar';
import Typography from 'material-ui/Typography';
import Chart from './components/HorizontalStackedBarChart';
import axios from 'axios';
import SimpleTable from './components/Table';
import Paper from 'material-ui/Paper';

import Grid from 'material-ui/Grid';
import ControlledOpenSelect from './components/Select';
import ClientChart from './components/ClientAnalysisChart';

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
  generalPaper: {
    marginLeft: 10,
    paddingTop: 15,
    paddingLeft: 10,
    marginTop: 10,
  },
  tablePaper: {
    marginLeft: 110,
  }
};

class App extends Component {
  state = {
    data: [],
    products: [],
    user_types: [],
    display_nps_chart: true,
    client_data: [],
    display_client_chart: true,
  };

  componentWillUpdate = (nextProps, nextState) => {
    console.log('component will update');
    if (
      (this.props.dataSelect.product !== nextProps.dataSelect.product) ||
      (this.props.dataSelect.user_type !== nextProps.dataSelect.user_type)
    ) {
      if (nextProps.dataSelect.product === '') {
        // Get data from the surveys endpoint
        const get_url = '/survey?users=' + nextProps.dataSelect.user_type;
        console.log(get_url);
        axios.get(get_url)
          .then(res => {
            console.log(res.data);
            this.setState({data: res.data});
          })
      }
      // get data from the products endpoint
      else {
        const get_url = '/product_data?product=' + nextProps.dataSelect.product +
          '&users=' + nextProps.dataSelect.user_type;
        console.log(get_url);
        axios.get(get_url)
          .then(res => {
            console.log(res.data);
            this.setState({data: res.data});
          })
      }
    }
  };

  componentWillMount() {
    console.log('component will mount');
    // Get initial data - survey with no selections
    axios.get('/survey?users=all')
      .then(res => {
        console.log(res);
        this.setState({data: res.data});
      });
    // Get list of products for select purposes
    axios.get('/products')
      .then(res => {
        this.setState({products: res.data});
      });
    //Get list of user types for select purposes
    axios.get('/user_types')
      .then(res => {
        this.setState({user_types: res.data});
      });
    axios.get('/client_deltas?survey=2018%20February&users=all')
      .then(res=> {
        this.setState({client_data: res.data});
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
              <Grid container className={classes.generalPaper}>
                <Grid container className={classes.generalPaper}>
                <Typography variant={'headline'}>Survey Comparisons</Typography>
                </Grid>
                {(this.state.display_nps_chart) ?
                <Grid item xs={6} className={classes.generalPaper}>
                  <Chart nps_data={this.state.data} width={800} height={300}/>
                </Grid>
                  :null }
                <Grid item xs={2} className={classes.generalPaper}>
                  <ControlledOpenSelect
                    menuList={this.state.products}
                    instructions={'Select the Product to View'}
                    name='product'
                    include_none={true}
                    val={this.props.dataSelect.product}
                  />
                </Grid>
                <Grid item xs={2} className={classes.generalPaper}>
                  <ControlledOpenSelect
                    menuList={this.state.user_types}
                    instructions={'Select the user types to View'}
                    name='user'
                    include_none={false}
                    val={this.props.dataSelect.user_type}
                  />
                </Grid>
              </Grid>
              <Grid container className={classes.generalPaper}>
                <Paper className={classes.tablePaper}>
                <SimpleTable
                  data={this.state.data}
                />
                </Paper>
              </Grid>
              <Grid container className={classes.generalPaper}>
                <Grid container className={classes.generalPaper}>
                <Typography variant={'headline'}>Client Comparisons</Typography>
                </Grid>

                <ClientChart
                  data={this.state.client_data}
                  width={1200}
                  height={500}
                  yaxis={this.state.products}
                />
              </Grid>

          </Grid>
        </div>
      </MuiThemeProvider>
    );
  }
}

function mapStateToProps(state) {
  return {
    dataSelect: state.dataSelect,
  };
}

function mapDispatchToProps(dispatch) {
  return {}
}

App.propTypes = {
  classes: PropTypes.object.isRequired,
  theme: PropTypes.object.isRequired,
};


export default withStyles(styles, {withTheme: true})(connect(mapStateToProps, mapDispatchToProps)(App));
