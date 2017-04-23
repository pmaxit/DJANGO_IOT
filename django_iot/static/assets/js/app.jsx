import React, { Component } from 'react';
import Pusher from 'pusher-js';

Pusher.logToConsole = true

var pusher = new Pusher('a9603eebc0a6a7c05d7e', {
  encrypted: true
});

class TableRow extends Component{
    constructor(props){
        super(props);
    }
    render(){
        const {data} = this.props;
        let transformData = []
        
        Object.keys(data).forEach((v,i) => {
            let finalData = {}
            finalData['id'] = i
            finalData['name'] = v
            finalData['value'] = data[v]

            transformData.push(finalData)
        })

        const row = transformData.map((d) =>
            <tr key={d.id}>
                <td key={d.name}>{d.name} </td>
                <td key={d.value}>{d.value} </td>
            </tr>
        );
        
        return <tbody>{row}</tbody>;
    }
};

class Table extends Component{
    
    constructor(props){
        super(props)
        this.pusher = new Pusher('a9603eebc0a6a7c05d7e', {
                encrypted: true
        });
        this.channel = this.pusher.subscribe('messages');
        console.log("PROPS 1 " , this.props);
        this.state = {
            data: this.props.data
        }
    }

    updateEvents(data){
        this.setState({
            data: data
        })
    }

    componentDidMount(){
        this.channel.bind('update',this.updateEvents.bind(this));
    }

    render(){
        return (
            <table className="table">
                 <thead>
                        <tr>
                            <th> Parameter </th>
                            <th> Value     </th>
                        </tr>
                    </thead>
                    <TableRow data={this.state.data} />
            </table>
        )
    }
}

Table.defaultProps = {
    data : 
            {
                "Device Internet Connection":  "OK",
                "Average Power Usage": "23.3 Watt / day",
                "Average Daily Usage": "12 hours / day",
                "Estimated bill"     : "$30"
            }
    }

export default Table;