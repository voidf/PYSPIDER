import React from 'react';
import {AppBar, Toolbar, Grid, Card, CardContent, CircularProgress, CardMedia, Typography, TextField, Button} from "@material-ui/core"
import { makeStyles, fade } from '@material-ui/core/styles';
import axios from "axios"
import { useState } from 'react';
import { useEffect } from 'react';
import SearchIcon from "@material-ui/icons/Search"
import { toFirstCharUpperCase } from "../utils/constants";
import SaveIcon from '@material-ui/icons/Save';

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



const Master = (props) => {

    const {history} = props
    const [pokemonData,setPokemonData] = useState()
    const [filter,setFilter] = useState("")

    const classes = useStyles()

    // const initButtons = 

    return (
        <>
        <AppBar position="static">
            <Toolbar>
                
                <Button 
                    variant="contained" 
                    color="default"
                    startIcon={<SaveIcon />}
                    size="large"
                    onClick = {()=>{alert("??")}}
                >爬</Button>
            </Toolbar>
        </AppBar>
            
        </>
    );
};

export default Master;