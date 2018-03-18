const styles = theme => ({
  root: {
    flexGrow: 1,
  },
  generalPaper: {
    marginLeft: 10,
    marginTop: 10,
  },
  tablePaper: {
    marginLeft: 15,
    marginTop: 30,
  },
  chartContainer: {
    marginTop: 0,
    marginLeft: 15,
  },
  selectorContainer: {
    marginLeft: 15,
    marginTop: 20,
  },
    button: {
    display: 'block',
    marginTop: theme.spacing.unit * 2,
  },
  formControl: {
    margin: theme.spacing.unit,
    minWidth: 120,
  },
  tableRoot: {
    width: '100%',
    overflowX: 'auto',
  },
  table: {
    minWidth: 100,
  },
  content: {
    width: '100%',
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    padding: 24,
    height: 'calc(100% - 56px)',
    marginTop: 24,
    [theme.breakpoints.up('sm')]: {
      height: 'calc(100% - 64px)',
      marginTop: 24,
    },
  },
});

export default styles;