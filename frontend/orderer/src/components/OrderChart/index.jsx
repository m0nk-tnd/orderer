import * as React from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import {Line} from 'react-chartjs-2';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);


export default function OrderChart(props) {
    const items = props.items || [];

    let dd = items.map((row) => (
        {
            "y": parseFloat(row.cost),
            "x": row.delivery_date
        }
    ))

    const data = {
        datasets: [
            {
                label: 'Orders',
                data: dd,
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.5)',
            },
        ],
    };

    if (items.length) {
        return (
            <Line data={data}/>
        );
    }

    return null;
}
