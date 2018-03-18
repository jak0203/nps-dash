import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import Table, { TableBody, TableCell, TableHead, TableRow } from 'material-ui/Table';
import Paper from 'material-ui/Paper';
import {selectHandleChange} from "../actions/select";
import {bindActionCreators} from "redux";

import {connect} from 'react-redux';
import styles from '../Styles';


function SimpleTable(props) {
  const { classes } = props;
  const {data} = props;

  return (
    <Paper className={classes.tableRoot}>
      <Table className={classes.table}>
        <TableHead>
          <TableRow>
            <TableCell>Survey</TableCell>
            <TableCell numeric>Total Responses</TableCell>
            <TableCell numeric>Detractors</TableCell>
            <TableCell numeric>Neutral</TableCell>
            <TableCell numeric>Promoters</TableCell>
            <TableCell numeric>Positve Clients</TableCell>
            <TableCell numeric>Negative Clients</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.concat().reverse().map(n => {
            return (
              <TableRow key={n.survey}>
                <TableCell>{n.survey}</TableCell>
                <TableCell numeric>{(n.total_responses)}</TableCell>
                <TableCell numeric>{(n.detractors)}</TableCell>
                <TableCell numeric>{(n.neutral)}</TableCell>
                <TableCell numeric>{(n.promoters)}</TableCell>
                <TableCell numeric>{(n.num_clients_positive)}</TableCell>
                <TableCell numeric>{(n.num_clients_negative)}</TableCell>
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