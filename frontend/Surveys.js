class Surveys extends React.Component {
    constructor(prop){
        super(prop);
        this.state={
            view: false,
        }
    }



    render(){
        let TrySurveys = [
            {
                title: "what is your name?",
                id: {},
                content: "content 1",
            },
            {
                title: "what is your name?",
                id: {},
                content: 'content 2',
            },
            
        ];
        const SurverOpened=()=>{
            this.setState({view: !this.state.view})
        }
        
        // const DisplayContent=()=>{
        //     const content = [];

        //     for (let i = 0; i < TrySurveys.length; i++) {
        //         content.push(<div>{TrySurveys[i].content}</div>);
        //     }
        //     return (content);
        // };
            return(
                <div>
                    {
                        TrySurveys.map((item,index)=>{
                            return(
                                <>
                                    <div className="Survey">
                                        <h2 className="Survey-title">{item.title}</h2>
                                        <input type='button' className='open' onClick={SurverOpened} value={`Open ${index+1}`}></input>

                                        <div id='content' className={(this.state.view == false)?('hide-fields'):('show-fields')}>
                                            {item.content}
                                        </div>
                                    </div>
                                </>
                            )
                        })
                    }
                </div>
            )
        

            // TrySurveys.map((item, index)=>{
            //     return(                                
            //         <div>
            //             {item.cName}
            //         </div>                    
            //     )
            // })
    }
}