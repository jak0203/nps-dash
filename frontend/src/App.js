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
import Tabs, {Tab} from 'material-ui/Tabs';
import ClientBreakdownChart from './components/ClientBreakdownChart';
import styles from './Styles';

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


function TabContainer(props) {
  return (
    <Typography component="div" style={{padding: 8 * 3}}>
      {props.children}
    </Typography>
  );
}

class App extends Component {
  state = {
    data: [],
    products: [],
    user_types: [],
    client_data: [],
    surveys: [],
    chart: 'surveyComparisons',
    value: 0,
  };

  componentWillUpdate = (nextProps, nextState) => {
    if (
      (this.props.dataSelect.product !== nextProps.dataSelect.product) ||
      (this.props.dataSelect.user_type !== nextProps.dataSelect.user_type)
    ) {
      if (nextProps.dataSelect.product === '') {
        // Get data from the surveys endpoint
        const get_url = '/survey_data?users=' + nextProps.dataSelect.user_type;
        axios.get(get_url)
          .then(res => {
            this.setState({data: res.data});
          })
      }
      // get data from the products endpoint
      else {
        const get_url = '/product_data?product=' + nextProps.dataSelect.product +
          '&users=' + nextProps.dataSelect.user_type;
        axios.get(get_url)
          .then(res => {
            this.setState({data: res.data});
          })
      }
    }
    if (this.props.dataSelect.survey !== nextProps.dataSelect.survey) {
      const get_url = 'client_deltas?survey=' + nextProps.dataSelect.survey + '&users=all'
      axios.get(get_url)
        .then(res=> {
          console.log(res.data);
          this.setState({client_data: res.data});
        })
    }
  };

  componentWillMount() {
    // Get initial data - survey with no selections
    axios.get('/survey_data?users=all')
      .then(res => {
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
      .then(res => {
        this.setState({client_data: res.data});
      });
    axios.get('/surveys')
      .then(res => {
        this.setState({surveys: res.data});
      });
  }

  handleChange = (event, value) => {
    this.setState({value});
  };

  render() {
    const {classes} = this.props;
    return (
      // App Bar
      <MuiThemeProvider theme={theme}>
        <div className={classes.root}>
          <AppBar position="fixed" color="default">
            <Toolbar>
              <Grid item xs={2}>
                <Typography variant="title" color="inherit">
                  NPS Dashboard
                </Typography>
              </Grid>
              <Grid item xs={10}>
                <Tabs value={this.state.value} onChange={this.handleChange}>
                  <Tab label={"Survey Comparisons"}/>
                  <Tab label={"Client Comparisons"}/>
                </Tabs>
              </Grid>
            </Toolbar>
          </AppBar>
        </div>

        <div className={classes.content}>
          {this.state.value === 0 &&
          <TabContainer>
            <Grid container className={classes.generalPaper}>

              <Grid container>
                <Grid item xs={6} md={2} className={classes.selectorContainer}>
                  <ControlledOpenSelect
                    menuList={this.state.products}
                    instructions={'Select the product to view'}
                    name='product'
                    include_none={true}
                    val={this.props.dataSelect.product}
                  />
                </Grid>
                <Grid item xs={6} md={2} className={classes.selectorContainer}>
                  <ControlledOpenSelect
                    menuList={this.state.user_types}
                    instructions={'Select the user types to view'}
                    name='user'
                    include_none={false}
                    val={this.props.dataSelect.user_type}
                  />
                </Grid>
              </Grid>

              <Grid container className={classes.tablePaper}>
                <Grid item lg={5}>

                <Chart
                  nps_data={this.state.data}
                  width={650}
                  height={300}
                /></Grid>
              <Grid item lg={5}>
              <ClientBreakdownChart
                  data={this.state.data}
                  width={650}
                  height={300}
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
            </Grid>
          </TabContainer>}

          {this.state.value === 1 && <TabContainer>
            <Grid container className={classes.selectorContainer}>
              <ControlledOpenSelect
              menuList={this.state.surveys}
              instructions={'Select the survey to view'}
              name={'survey'}
              include_none={false}
              val={this.props.dataSelect.survey}
              />
            </Grid>
            <Grid container className={classes.chartContainer}>
              <ClientChart
                data={this.state.client_data}
                width={1200}
                height={500}
                yaxis={this.state.products}
              />
            </Grid>

          </TabContainer>}
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
