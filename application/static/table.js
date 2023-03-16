const {Table} = window.antd;



function AndTables(props){
    const dataSource = [
        {
          key: '1',
          name: 'Mike',
          age: 32,
          address: '10 Downing Street',
        },
        {
          key: '2',
          name: 'John',
          age: 42,
          address: '10 Downing Street',
        },
      ];
      
      const columns = [
        {
          title: 'Name',
          dataIndex: 'name',
          key: 'name',
        },
        {
          title: 'Age',
          dataIndex: 'age',
          key: 'age',
        },
        {
          title: 'Address',
          dataIndex: 'address',
          key: 'address',
        },
      ];

    return (<div>
           <Table dataSource={props.dataSource} columns={props.columns} />; 
        </div>)
}

// function Welcome(props) {
//     return <h1>Hello, {props.name}</h1>;
//   }

const table = {
    render: (dataSource, data) => {
        console.log(data, dataSource)
        const domContainer = document.querySelector('#reactDiv');
        const root = ReactDOM.createRoot(domContainer);
        root.render(<AndTables dataSource={dataSource} columns={data}></AndTables>);
    }
}
