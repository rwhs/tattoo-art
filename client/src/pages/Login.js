import React, { Component } from "react";
import { Header } from "./Header";
import { LoginPageButton } from "./LoginPageButton";
import { LoginPaper } from "./LoginPaper";
import { BasicTextField } from "./TextField";
import { Grid, Typography } from "@material-ui/core";

class Login extends Component {
  constructor(props) {
    super(props);

    this.state = {
      email: '',
      password: '',
      error: ''
    }

    this.handleFormSubmit = this.handleFormSubmit.bind(this)
    this.handleEmailChange = this.handleEmailChange.bind(this)
    this.handlePasswordChange = this.handlePasswordChange.bind(this)
    this.handleLogout = this.handleLogout.bind(this)
  }

  // Handlers
  handleFormSubmit(e) {
    e.preventDefault();

    fetch('http://localhost:5000/login', { // POST request to backend
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        "email": this.state.email,
        "password": this.state.password
      })
    })
      .then(response => response.json())
      .then(response => {
        if (response.token) {
          localStorage.setItem('token', response.token)
          this.props.history.push('/') // Redirect to home page
        } else {
          this.setState({ error: response.error });
        }
      })
  }

  handleEmailChange(emailInput) {
    this.setState({ email: emailInput })
  }

  handlePasswordChange(passwordInput) {
    this.setState({ password: passwordInput })
  }

  handleLogout() {
    localStorage.removeItem('token');
    window.location.reload()
  }

  render() {
    return (
      <div>
        <Header />
        <LoginPaper>
          <Grid container direction="column" alignContent="center">
            <form onSubmit={this.handleFormSubmit}>
              <BasicTextField
                label="E-mail"
                value={this.state.email}
                onChange={e => this.handleEmailChange(e.target.value)}
              />
              <BasicTextField
                type="password"
                label="Password"
                value={this.state.password}
                onChange={e => this.handlePasswordChange(e.target.value)}
              />
              <Grid item>
                <Typography variant="caption" color="primary">
                  {/* add functionality for forgetting password */}
                  <a href="">
                    Forgot Your Password?
                  </a>
                </Typography>
              </Grid>
              <LoginPageButton type="submit" />
            </form>
            <p>{this.state.error}</p>
          </Grid>
        </LoginPaper>
      </div>
    )
  }
}

export default Login;
