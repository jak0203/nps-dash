import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import { InputLabel } from 'material-ui/Input';
import { MenuItem } from 'material-ui/Menu';
import { FormControl } from 'material-ui/Form';
import Select from 'material-ui/Select';
import Typography from 'material-ui/Typography';

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
    const {
      menuList,
      instructions,
      name,
      include_none,
      val
    } = this.props;

    return (
      <form autoComplete="off">
        <Typography variant={'subheading'}>
          { instructions }
        </Typography>
        <FormControl className={classes.formControl}>
          <InputLabel htmlFor="controlled-open-select"></InputLabel>
          <Select
            open={this.state.open}
            onClose={this.handleClose}
            onOpen={this.handleOpen}
            value={val}
            onChange={this.props.selectHandleChange}
            inputProps={{
              name: name,
              id: 'controlled-open-select',
            }}
          >
            {(include_none) ?
              <MenuItem value=''>
                <em>None</em>
              </MenuItem> : null
            }
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
    dataSelect: state.dataSelect,
  }
}

function mapDispatchToProps(dispatch) {
  return {
    selectHandleChange: bindActionCreators(selectHandleChange, dispatch)
  }
}

export default withStyles(styles)(connect(mapStateToProps, mapDispatchToProps)(ControlledOpenSelect));
