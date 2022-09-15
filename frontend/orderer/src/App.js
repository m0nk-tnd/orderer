import './App.css';

import * as React from 'react';

import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';

import OrderList from './components/OrderList';
import OrderChart from './components/OrderChart';
import {fetchOrders} from './fetches';


function App() {

    const [orders, setOrders] = React.useState([]),
        [total, setTotal] = React.useState([]);

    React.useEffect(() => {
        fetchOrders(setOrders, setTotal);
    }, []);

    return (
        <Container maxWidth="lg" className="App">
            <Grid container spacing={2}>
                <Grid item xs={6}>
                    <OrderChart items={orders}/>
                    <Paper elevation={3}>
                        <Typography variant="h3" gutterBottom>
                            Total
                        </Typography>
                        <Typography variant="h5" gutterBottom>
                            {total}
                        </Typography>
                    </Paper>
                </Grid>
                <Grid item xs={6}>
                    <OrderList items={orders}/>
                </Grid>
            </Grid>
        </Container>
    );
}

export default App;
