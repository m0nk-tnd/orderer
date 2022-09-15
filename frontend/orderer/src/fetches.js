import config from './config.json';

const api_url = config.API_HOST;


export async function fetchOrders(setOrdersCallback, setTotalCallback) {
    let headers = {
        'Content-Type': 'application/json'
    };

    return fetch(`${api_url}/order`, {
        cache: 'no-cache',
        headers: headers,
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            setOrdersCallback(data.orders);
            setTotalCallback(data.total);
            return data;
        });
}
