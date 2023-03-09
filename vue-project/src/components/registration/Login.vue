<template>
    <div>
        
        <FormulateForm
            @submit="sendLoginInfoClick"
            #default="{ hasErrors }"
        >
            <FormulateInput ref="formulate-input-username" v-model='username' type="text" label="Username" name="username" validation="required" ></FormulateInput>
            <FormulateInput ref="formulate-input-password" v-model='password' type="password"  label="Password" name="password" validation="required" ></FormulateInput>
            
            <FormulateInput type="submit" :disabled="hasErrors">
                Login
            </FormulateInput>

        </FormulateForm>

    </div>
</template>


<script>

import Cookies from "universal-cookie";
import axios from 'axios'
import { Buffer } from 'buffer';


export default {
    data () {
        return {
            username:'',
            password:'',
        }

    },
    
    methods : {
        
        sendLoginInfoClick(data){
            console.log(data)
            let username = this.username
            let password = this.password
            console.log(username, password)
            // const cookies = new Cookies();
            const token = Buffer.from(`${username}:${password}`, 'utf8').toString('base64')

            // fetch(this.$API_URL+"login", {
            //     method: "POST",
            //     headers: {
            //         "Content-Type": "application/json",
            //         "X-CSRFToken": this.$cookies.get("csrftoken"),
            //     },
            //     credentials: "include",
            //     body: JSON.stringify({username: username, password: password}),
            // }).then((response)=>{
            //         alert(response.data)
            // })

            

            


            axios.defaults.xsrfCookieName = 'csrftoken'
            axios.defaults.xsrfHeaderName = "X-CSRFToken"
            axios.defaults.withCredentials = true;
            axios({
                method: 'post',
                url: this.$API_URL+"login",
                xsrfCookieName: 'csrftoken',
                xsrfHeaderName: 'X-CSRFToken',
                headers : {
                    'X-CSRFToken': 'csrftoken',
                    'Authorization' :`Basic ${token}`
                },
                // withCredentials : true,

            }).then((response)=>{
                    alert(response.data)
            })


        }


    }
}
</script>



