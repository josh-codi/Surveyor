class AdminPage extends React.Component {
    constructor(prop){
        super(prop);
        this.state={
            switch: 0,
        }
    }


    render(){
        const createClick=()=>{
            this.setState({switch: 1})
        }
        const submissionClick=()=>{
            this.setState({switch: 2})
        }
        
            if(this.state.switch==0){
                return(
                    <div className="admin-container">
                        <button className="create-btn" onClick={createClick}>create</button>
                        <button className="submissions-btn" onClick={submissionClick}>submissions</button>
                    </div>
                )
            }
            else if(this.state.switch==1){
                return(
                    <div>
                        <AdminCreateSurvey/>
                    </div>
                )
            }
            else if(this.state.switch==2){
                return(
                    <div>
                        <Surveys/>
                    </div>
                )
            }
            
        
    }
}