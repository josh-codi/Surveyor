// class LandingPage extends React.Component {
//     constructor(prop){
//         super(prop);
//         this.state={
//             move: 0,
//         }
//     }

//     render(){
//         return(
//             <h2>what</h2>
//         )
//     }
// }














class LandingPage extends React.Component {
    constructor(prop){
        super(prop);

        this.state={
            move: 0,
            username: '',
            password: '',
            error: ''
        }
    }



    render(){
        const clicked_1 = ()=>{
            if(this.state.username == 'master' && this.state.password == 'keypass'){
                this.setState({move: 1})
            }else{
                alert('You inputed wrong credentials')
            }
            
        };

        const clicked_2 = ()=>{
            this.setState({move: 2})
        };
        
        const clicked_3 = ()=>{
            this.setState({move: 0})
        };

        if(this.state.move == 0){
            return(
                <div className='landing-page'>   
                    <h4>Admin Login</h4>
                          <form className='admin-login'>
                              <label for="username">Username</label><br/>
                              <input type='text' name='username'onChange={(e)=>{this.setState({username: e.target.value})}}/><br/><br/>

                              <label for="password">Password</label><br/>
                              <input type='password' name='password'onChange={(e)=>{this.setState({password: e.target.value})}}/><br/><br/>

                              <button className="Admin-btn" onClick={clicked_1}>Admin Login</button>
                          </form><br/><br/>
                          <h4>
                              Continue as a Survey Partner
                          </h4>
                          <button className="User-btn" onClick={clicked_2}>Continue</button>
                </div>
            )
        }else if(this.state.move == 1){
            return(
                <div>
                <AdminPage/><br/>
                <button className="logout" onClick={clicked_3}>Logout</button>
                </div>
                
            )
        }else if(this.state.move == 2){
            return(
                <div>
                <UsersPage/><br/>
                <button className="go-back" onClick={clicked_3}>Go Back</button>
                </div>
            )
        }
            
    }
        
}