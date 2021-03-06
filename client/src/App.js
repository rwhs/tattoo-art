import React from "react";
import { MuiThemeProvider } from "@material-ui/core";
import { MuiPickersUtilsProvider } from '@material-ui/pickers';
import { BrowserRouter, Route, Switch } from "react-router-dom";
import DateFnsUtils from '@date-io/date-fns';

import { theme } from "./themes/theme";
import HomePage from "./pages/HomePage";
import Payments from "./pages/Payments";
import Login from "./pages/Login";
import CreateContest from "./pages/CreateContest";
import Signup from "./pages/Signup";
import { UploadSubmission } from './pages/UploadSubmission';
import { ViewSubmissions } from './pages/ViewSubmissions';
import { ViewContest } from './pages/ViewContest';
import { Messaging } from "./pages/Messaging";
import Profile from './pages/Profile';

import "./App.css";

function App() {
  return (
    <MuiPickersUtilsProvider utils={DateFnsUtils}>
      <MuiThemeProvider theme={theme}>
        <BrowserRouter>
          <Switch>
            <Route exact path="/" component={HomePage} />
            <Route path="/login" component={Login} />
            <Route path="/signup" component={Signup} />
            <Route path="/payments-demo" component={Payments} />
            <Route path="/upload-submission/:contestID" component={UploadSubmission} />
            <Route path="/view-submissions/:contestID" component={ViewSubmissions} />
            <Route path="/view-contest" component={ViewContest} />
            <Route path="/create-contest" component={CreateContest} />
            <Route path="/profile" component={Profile} />
            <Route path="/messages" component={Messaging} />
          </Switch>
        </BrowserRouter>
      </MuiThemeProvider>
    </MuiPickersUtilsProvider>
  );
}

export default App;
