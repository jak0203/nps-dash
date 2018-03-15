import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import Table, { TableBody, TableCell, TableHead, TableRow } from 'material-ui/Table';
import Paper from 'material-ui/Paper';
import {selectHandleChange} from "../actions/select";
import {bindActionCreators} from "redux";

import {connect} from 'react-redux';

const styles = theme => ({
  root: {
    width: '100%',
    marginTop: theme.spacing.unit * 3,
    overflowX: 'auto',
  },
  table: {
    maxWidth: 690,
  },
});


function SimpleTable(props) {
  const { classes } = props;
  const {data} = props;

  return (
    <Paper className={classes.root}>
      <Table className={classes.table}>
        <TableHead>
          <TableRow>
            <TableCell>Survey</TableCell>
            <TableCell numeric>Total Responses</TableCell>
            <TableCell numeric>% Detractors</TableCell>
            <TableCell numeric>% Neutral</TableCell>
            <TableCell numeric>% Promoters</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.reverse().map(n => {
            return (
              <TableRow key={n.survey}>
                <TableCell>{n.survey}</TableCell>
                <TableCell numeric>{(n.total_responses)}</TableCell>
                <TableCell numeric>{(n.percent_detractors).toFixed(2)}</TableCell>
                <TableCell numeric>{(n.percent_neutral).toFixed(2)}</TableCell>
                <TableCell numeric>{(n.percent_promoters).toFixed(2)}</TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </Paper>
  );
}

SimpleTable.propTypes = {
  classes: PropTypes.object.isRequired,
};

function mapStateToProps(state) {
  return {
    productSelect: state.productSelect,
  }
}

function mapDispatchToProps(dispatch) {
  return {
    selectHandleChange: bindActionCreators(selectHandleChange, dispatch)
  }
}

export default withStyles(styles)(connect(mapStateToProps, mapDispatchToProps)(SimpleTable));