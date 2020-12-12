import React from 'react';
import { Link } from 'react-router-dom';
import { makeStyles, Button, Typography } from '@material-ui/core';

const useStyles = makeStyles(theme => ({
  button: {
    backgroundColor: "white",
    borderRadius: "0",
    color: "black",
    width: "6rem",
    padding: theme.spacing(1.5, 2),
  },
  title: {
    fontFamily: theme.fontFamily,
    fontSize: 12,
  },
  buttonContainer: {
    marginLeft: "auto",
    marginRight: "auto",
  }
}));

export function SignUpButton() {
  const classes = useStyles();

  return (
    <div className={classes.buttonContainer}>
      <Button className={classes.button} component={ Link } to="/signup" color="inherit" variant="contained">
        <Typography className={classes.title}>
          Sign Up
        </Typography>
      </Button>
    </div>
  )
}