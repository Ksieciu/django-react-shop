import React from 'react'
import { useState, useEffect } from 'react'
import { Button, Row, Col, ListGroup, Image, Card } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import Message from '../components/Message'
import Loader from '../components/Loader'
import { getOrderDetails } from '../actions/orderActions'


function OrderScreen({ match }) {
    const orderId = match.params.id
    const dispatch = useDispatch()

    const orderDetails = useSelector(state => state.orderDetails)
    const { order, error, loading } = orderDetails

    if(!loading && !error){
        order.itemsPrice = order.orderItems.reduce((acc, item) => acc + item.price * item.quantity, 0).toFixed(2)
    }

    useEffect(() => {
        if(!order || order.id !== Number(orderId)){
            dispatch(getOrderDetails(orderId))
        }
    }, [dispatch, order, orderId])

    return loading ? (
        <Loader/>
    ) : error ? (
        <Message variant='danger'>{error}</Message>
    ) : (
        <div>
            <h1>Order: {order.id}</h1>
            <Row>
                <Col md={8}>
                    <ListGroup variant='flush'>
                        <ListGroup.Item>
                            <h2>Shipping</h2>
                            <p><strong>Name:</strong> {order.user.name} </p>
                            <p><strong>Email:</strong><a href={`mailto:${order.user.email}`}> {order.user.email}</a> </p>
                            <p>
                                <strong>Shipping: </strong>
                                {order.shipping_address.address}, {order.shipping_address.city}
                                {'   '}
                                {order.shipping_address.postcode},
                                {'   '}
                                {order.shipping_address.country},
                            </p>
                            <Message variant='success'>{order.status}</Message>
                            
                        </ListGroup.Item>

                        <ListGroup.Item>
                            <h2>Payment Method</h2>

                            <p>
                                <strong>Method: </strong>
                                {order.payment_method}
                            </p>
                            {order.payment_done ? (
                                <Message variant='success'>Paid on {order.payment_date}</Message>
                            ) : (
                                <Message variant='warning'>Not Paid</Message>
                            )}
                        </ListGroup.Item>

                        <ListGroup.Item>
                            <h2>Order Items</h2>
                            {order.orderItems.length === 0 ? <Message variant='info'>
                                Your order is empty!
                            </Message> : (
                                <ListGroup variant='flush'>
                                    {order.orderItems.map((item, index) => (
                                        <ListGroup.Item key={index}>
                                            <Row>
                                                <Col md={2}>
                                                    <Image src={item.image} alt={item.name} fluid rounded />
                                                </Col>

                                                <Col>
                                                    <Link to={`/products/${item.product}`}>{item.name}</Link>
                                                </Col>

                                                <Col>
                                                    {item.quantity} * ${item.price} = ${(item.quantity * item.price).toFixed(2)}
                                                </Col>
                                            </Row>
                                        </ListGroup.Item>
                                    ))}
                                </ListGroup>
                            )}
                        </ListGroup.Item>
                        
                    </ListGroup>
                </Col>

                <Col md={4}>
                    <Card>
                        <ListGroup variant='flush'>
                            <ListGroup.Item>
                                <h2>Order Summary</h2>
                            </ListGroup.Item>

                            <ListGroup.Item>
                                <Row>
                                    <Col>Items: </Col>
                                    <Col>${order.itemsPrice}</Col>
                                </Row>
                            </ListGroup.Item>

                            <ListGroup.Item>
                                <Row>
                                    <Col>Includes Tax: </Col>
                                    <Col>${order.tax_amount}</Col>
                                </Row>
                            </ListGroup.Item>

                            <ListGroup.Item>
                                <Row>
                                    <Col>Shipping: </Col>
                                    <Col>${order.shipping_price}</Col>
                                </Row>
                            </ListGroup.Item>
                            
                            <ListGroup.Item>
                                <Row>
                                    <Col>Total: </Col>
                                    <Col>${order.total_price}</Col>
                                </Row>
                            </ListGroup.Item>
                        </ListGroup>
                    </Card>
                </Col>
            </Row>
        </div>
    )
}

export default OrderScreen
