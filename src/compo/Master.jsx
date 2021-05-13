import React from 'react';
import {Box, AppBar, Toolbar, Grid, Card, CardContent, CircularProgress, CardMedia, Typography, TextField, Button, Slider} from "@material-ui/core"
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
const baseurlocal = "http://localhost:8000/"

const Master = (props) => {

    const {history} = props
    const [ppt, setppt] = useState(30)
    const [filter,setFilter] = useState("")
    
    const classes = useStyles()
    


    return (
        <>
        <AppBar position="static">
            <Toolbar>
                
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
                        const uurl = baseurl+"load?prv="+ppt
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
                        axios.get(baseurl+"save?prv="+ppt).then(
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
                        const uurl = baseurl+"master?prv="+ppt;
                        
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


                   
                    {/* <TextField 
                        id="standard-basic" 
                        label="需要爬前多少天的数据？"
                        
                        fullWidth
                        style={{
                            margin:15
                        }}
                        color="secondary"
                    ></TextField> */}
            </Toolbar>
        </AppBar>
        <Card id="ASDF" style={{height:"100%"}}>

        </Card>
            
        </>
    );
};

export default Master;