
class AdminCreateSurvey extends React.Component {
    constructor(prop){
        super(prop);
        this.state={
            number_of_fields: null,
            submited: false,
            title: null
        }
    }

    render(){

        const submit=()=>{
            localStorage.setItem('numberOfField',`${this.state.number_of_fields}`);
            this.setState({submited: true})
        }

        if(this.state.submited == false){
            return(
            <div>
                 <h1>Admin Create Survey</h1>
                 <p>Input the number of fields of which you want to create</p>
                 <input onChange={(e)=>{this.setState({number_of_fields: e.target.value})}} value={this.state.number_of_fields}/>
                 <button onClick={(submit)}>Submit</button>
                 <br/>
            </div>
            )
        }else{
            return(               
                   <div>
                       <Fields the_number_to_create={this.state.number_of_fields}/>                       
                   </div>       
            )
        }
        
}
}