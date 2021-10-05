class Fields extends React.Component {
    constructor(props){
        super(props);

    }

    render(){
        const number_to_create=this.props.the_number_to_create;

        const create = () => {
            const sec=[];
            for(let i=0;i<number_to_create;i++){
                sec.push(
                    <div className='fields'>
                        <label for="label">Type the Input field's label here</label><br/>
                    <input type="text" name="label" placeholder="Input field's label"/><br/>
                    <div>
                    <label for="type">Choose the user input type</label><br/>
                    <select name="type" id="type">
                        <option value="text">text</option>
                        <option value="number">number</option>
                    </select>
                    </div>
                    
                    </div>
                )
                
            }
            return (sec)
        }
        return(
            <>
                <div>
                    {(create)()}
                <button className="complete-form">Complete Form</button>
                </div> <br/><br/>   
            </>
        )
    }
}