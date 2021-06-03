import React from 'react';
import { Menu, MenuItem, Tab, ListSubheader,Divider,ListItemIcon,List,ListItem,ListItemText,Box, AppBar, Toolbar, Grid, Card, CardContent, CircularProgress, CardMedia, Typography, TextField, Button, Slider, Tabs} from "@material-ui/core"
import { makeStyles, fade } from '@material-ui/core/styles';
import axios from "axios"
import { useState } from 'react';
import { useEffect } from 'react';
import SearchIcon from "@material-ui/icons/Search"
import ReactDom from 'react-dom';
import { toFirstCharUpperCase } from "../utils/constants";
import SaveIcon from '@material-ui/icons/Save';
import ArrowDownwardIcon from '@material-ui/icons/ArrowDownward';
import EjectIcon from '@material-ui/icons/Eject';
import ArchiveIcon from '@material-ui/icons/Archive';
import {TrendingDown,TrendingUp,Brightness5, Alarm, AlarmOff, MonetizationOn} from '@material-ui/icons';

const useStyles = makeStyles(theme => ({
    pokedexContainer: {
        paddingTop:'20px',
        paddingLeft:'50px',
        paddingRight: '50px'
    },
    cardMedia: {
        margin : "auto"
    },
    cardContent : {
        textAlign:"center"
    },
    searchContainer: {
        display:`flex`,
        backgroundColor: fade(theme.palette.common.white, 0.15),
        paddingLeft: "20px",
        paddingRight: "20px",
        marginTop: "5px",
        marginBottom: "5px"
    },
    searchIcon: {
        alignSelf:"flex-end",
        marginBottom: "5px"
    },
    searchInput: {
        width: "200px",
        margin: "5px",
    }
}))

const baseurl = "http://rinko.work:7012/"
// const baseurl = "http://localhost:8000/"

const Master = (props) => {

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    
    const [cryptocurrenciesdata, setcrypto] = useState([]);
    const [currencytype, setcurrencytype] = useState('BTC');
    
    const [anchorEl, setAnchorEl] = useState(null);
    const {history} = props
    const [ppt, setppt] = useState(30)
    const [filter,setFilter] = useState("")
    
    const classes = useStyles()

    var extargs = [];
    
    const handleClose = (e) => {

        // console.log(e.target.innerText);
        
        setcurrencytype(e.target.innerText?e.target.innerText:'BTC')
        // extargs = ['typ='+currencytype]
        // console.log(extargs)

        setAnchorEl(null);
    };
    // await 

    useEffect(() =>  {
            axios.get(baseurl+'cryptocurrencies').then(
                resp => {
                    // console.log(resp.data);
                    setcrypto(resp.data)
                }
            ) 
        }
    ,[]);

    function generate_items()
    {
        // for(var coinsname in anchorEl)
        // console.log(cryptocurrenciesdata);
        var v =  Object.values(cryptocurrenciesdata).map(coinsname =>
            {
                // console.log(coinsname);
                return(<MenuItem onClick={handleClose}>{coinsname}</MenuItem>);
            }
        )
        // console.log(v);
        return v;
    }


    return (
        <>
        <AppBar position="static">

            <Toolbar>
                
                <Button 
                    variant="contained" 
                    color="secondary"
                    startIcon={<ArchiveIcon />}

                    size="large"
                    style={{
                        color:'#FFF',
                        width:'200px',
                        margin:5
                    }}
                    onClick = {()=>{
                        const uurl = baseurl+"info?ts="+Date.now()
                        axios.get(uurl).then(
                            resp => {
                                
                                ReactDom.render(
                                    <div>
                                    <List component="nav">
                                        <ListSubheader>
                                        <ListItem button>
                                                <ListItemText primary="日期" />
                                            {/* <ListItemIcon>
                                                <Brightness5 />
                                            </ListItemIcon> */}
                                                
                                            <ListItemIcon>
                                                <Alarm />
                                            </ListItemIcon>
                                            <ListItemText primary="开盘价" />

                                            <ListItemIcon>
                                                <AlarmOff />
                                            </ListItemIcon>
                                            <ListItemText primary="收盘价" />

                                            <ListItemIcon>
                                                <TrendingUp />
                                            </ListItemIcon>

                                            <ListItemText primary="最高价" />
                                            <ListItemIcon>
                                                <TrendingDown />
                                            </ListItemIcon>
                                            <ListItemText primary="最低价" />

                                        </ListItem></ListSubheader>
                                        <Divider />
                                        {
                                            Object.values(resp.data).map(
                                                (item1) => {
                                                    item1['date'] = new Date(parseFloat(item1['date'])*1000).toLocaleDateString()
                                                    console.log(Object.values(item1))
                                                    console.log(item1)
                                                    return (
                                                        <ListItem button >
                                                                <ListItemText primary={item1['date']} />
                                                                <ListItemText primary={"  \t\t"+item1['open']} />
                                                                <ListItemText primary={"  \t\t"+item1['close']} />
                                                                <ListItemText primary={"  \t\t"+item1['high']} />
                                                                <ListItemText primary={"  \t\t"+item1['low']} />
                                                        </ListItem >
                                                    )
                                                })
                                        }

                                    </List>
                                    </div>
                                
                                , document.querySelector("#ASDF"))
                            }
                        )
                    }}
                >库内数据</Button>

                <Button 
                    variant="contained" 
                    color="secondary"
                    startIcon={<EjectIcon />}
                    size="large"
                    style={{
                        color:'#FFF',
                        width:'180px',
                        margin:5
                    }}
                    onClick = {()=>{
                        const uurl = baseurl+"load?prv="+ppt+"&ts="+Date.now()+"&typ="+currencytype;
                        const a =(
                            <>
                                <Typography variant="h1">
                                    <img src={uurl} alt="" height="100%" width="100%" />
                                </Typography>

                            </>
                        );
                        ReactDom.render(a, document.querySelector("#ASDF"))
                    }}
                >读库</Button>

                <Button 
                    variant="contained" 
                    color="secondary"
                    startIcon={<SaveIcon />}
                    size="large"
                    style={{
                        color:'#FFF',
                        width:'180px',
                        margin:5
                    }}
                    onClick = {()=>{
                        axios.get(baseurl+"save?prv="+ppt +'&typ='+ currencytype).then(
                            resp=>{
                                console.log(resp);
                                alert("存库成功，当前记录数："+resp.data);
                            }
                        )
                        // alert()
                    }}
                >入库</Button>

                <Button 
                    variant="contained" 
                    color="secondary"
                    startIcon={<ArrowDownwardIcon />}
                    size="large"
                    style={{
                        color:'#FFF',
                        width:'180px',
                        margin:5
                    }}
                    onClick = {()=>{
                        const uurl = baseurl+"master?prv="+ppt+'&typ='+ currencytype;
                        
                        // axios.get("http://localhost:8000/master?prv="+ppt,
                        // {
                        //     headers:{
                        //         'Access-Control-Allow-Origin':'*'
                        //     },
                        //     responseType:'arraybuffer'
                        // }).then((response)=>{
                        //         return 'data:image/png;base64,' +btoa(new Uint8Array(response.data).reduce((data, byte) => data + String.fromCharCode(byte), ''));
                        //     }).then(data=>{
                        //         const a =(
                        //             <>
                        //                 <Typography variant="h1">
                        //                     <img src={data} alt="" />
                        //                 </Typography>
        
                        //             </>
                        //         );
                        //         ReactDom.render(a, document.querySelector("#ASDF"))
                        //     })
                            const a =(
                                <>
                                    <Typography variant="h1">
                                        <img src={uurl} alt="" height="100%" width="100%" />
                                    </Typography>
    
                                </>
                            );
                            ReactDom.render(a, document.querySelector("#ASDF"))

                        
                    }}
                >直接爬</Button>
                <Box style={{margin:"10px",width:"100%"}}>
                    <Typography id="discrete-slider" gutterBottom>
                        需要爬前多少天的数据？
                    </Typography>

                    <Slider
                        id="MX"
                        defaultValue={30}
                        aria-labelledby="discrete-slider"
                        valueLabelDisplay="auto"
                        step={10}
                        marks
                        min={10}
                        max={360}
                        color="secondary"
                        onChange={(e,val)=>{setppt(val)}}
                        
                    />
                </Box>

            </Toolbar>
            <Toolbar>
            <Button aria-controls="simple-menu" aria-haspopup="true" onClick={handleClick}
                variant="contained" 
                color="secondary"
                startIcon={<MonetizationOn />}
                size="large"
                style={{
                    color:'#FFF',
                    width:'150px',
                    margin:5
                }}>
                币种
            </Button>
            <Menu
                id="simple-menu"
                anchorEl={anchorEl}
                keepMounted
                open={Boolean(anchorEl)}
                onClose={handleClose}
            >
                {   
                    cryptocurrenciesdata?generate_items():<CircularProgress />
                }

            </Menu>
                
            </Toolbar>
        </AppBar>

        <Card id="ASDF" style={{height:"100%"}}>

        </Card>
            
        </>
    );
};

export default Master;