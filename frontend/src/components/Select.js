import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import { InputLabel } from 'material-ui/Input';
import { MenuItem } from 'material-ui/Menu';
import { FormControl } from 'material-ui/Form';
import Select from 'material-ui/Select';
import Button from 'material-ui/Button';

import {connect} from 'react-redux';
import {selectHandleChange} from '../actions/select';
import {bindActionCreators} from "redux";

const styles = theme => ({
  button: {
    display: 'block',
    marginTop: theme.spacing.unit * 2,
  },
  formControl: {
    margin: theme.spacing.unit,
    minWidth: 120,
  },
});

class ControlledOpenSelect extends React.Component {
  state = {
    open: false,
  };

  handleClose = () => {
    this.setState({ open: false });
  };

  handleOpen = () => {
    this.setState({ open: true });
  };

  render() {
    const { classes } = this.props;
    const { menuList } = this.props;
    return (
      <form autoComplete="off">
        <Button className={classes.button} onClick={this.handleOpen}>
          Select the Dataset to View
        </Button>
        <FormControl className={classes.formControl}>
          <InputLabel htmlFor="controlled-open-select"></InputLabel>
          <Select
            open={this.state.open}
            onClose={this.handleClose}
            onOpen={this.handleOpen}
            value={this.props.productSelect.product}
            onChange={this.props.selectHandleChange}
            inputProps={{
              name: 'Product',
              id: 'controlled-open-select',
            }}
          >
            <MenuItem value="">
              <em>None</em>
            </MenuItem>
            {menuList.map( ({value, display}) => {
              return(
                <MenuItem key={value} value={value}>{display}</MenuItem>
              )
            })}
          </Select>
        </FormControl>
      </form>
    );

  }
}

ControlledOpenSelect.propTypes = {
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

export default withStyles(styles)(connect(mapStateToProps, mapDispatchToProps)(ControlledOpenSelect));
