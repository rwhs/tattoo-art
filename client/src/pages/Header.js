import React from "react";
import { Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, makeStyles } from '@material-ui/core';
import { SignUpButton } from "./SignUpButton";

const useStyles = makeStyles(theme => ({
  title: {
    width: "100%",
    flexGrow: 1,
    marginLeft: theme.spacing(5),
    fontFamily: theme.fontFamily,
    letterSpacing: "0.3em",
    color: "inherit",
    textDecoration: "none"  
  },
  AppBar: {
    zIndex: theme.zIndex.drawer + 1,
    backgroundColor: "black"
  },
  offset: theme.mixins.toolbar
}));

export function Header(props) {
  const classes = useStyles();

  return (
    <div>
      <AppBar position="fixed" className={classes.AppBar}>
        <Toolbar>
          <Typography variant="h6" className={classes.title} component={ Link } to="/">
            TATTOO ART
          </Typography>
          {props.children}
          <SignUpButton />
          {localStorage.getItem('token')}
        </Toolbar>
      </AppBar>
      <div className={classes.offset} />
    </div>
  )
}