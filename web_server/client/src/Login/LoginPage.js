import React, { PropTypes }  from 'react';
import LoginForm from './LoginForm';

class LoginPage extends React.Component {
    constructor(props) {
        super();
        // set the initial component state
        this.state = {
            errors: {},
            user: {
                email: '',
                password: ''
            }
        };

        this.processForm = this.processForm.bind(this);
        this.changeUser = this.changeUser.bind(this);
    }
    
    // Pre-submission
    processForm(event) {
        event.preventDefault();

        const email = this.state.user.email;
        const password = this.state.user.password;

        // TODO: post login data
    }

    changeUser(event) {
         const field = event.target.name;
         const user = this.state.user;
         user[field] = event.target.value;
         // user['email'] = '123@123.com'
         // user['password'] = '123456789'
        this.setState({ user });
    }

    render() {
        return (
            <LoginForm 
                onSubmit={this.processForm}
                onChange={this.changeUser}
                errors={this.state.errors}
                user={this.state.user} />
        );
    }
}

export default LoginPage;