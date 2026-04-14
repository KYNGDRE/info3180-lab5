<template>
    <!-- Success Message --> 
<div v-if="successMessage" class="alert alert-success">
  {{ successMessage }}
</div>

<!-- Error Messages -->
<ul v-if="errors.length" class="alert alert-danger">
    <!-- <li v-for="error in errors"> -->
    <li v-for="(error, index) in errors" :key="index">
    {{ error }}
  </li>
</ul>
    <form @submit.prevent="saveMovie"  method="post" enctype="multipart/form-data"> 
        <!-- action="/api/v1/movies"      -->
        <div class="form-group mb-3">
            <label for="title" class="form-label">Movie Title</label>
            <input type="text" name="title" class="form-control" />
        </div>  
        <div class="form-group mb-3">         
            <label for="description">Message:</label>         
            <textarea id="description" name="description"></textarea>     
        </div>    
        <div class="form-group mb-3">         
            <!-- <label for="mail">E-mail:</label>         
            <input type="email" id="mail" name="email" />      -->
            <label for="poster">Choose the Movie Poster:</label>
            <input type="file" id="poster" name="poster" accept="image/*">
        </div>     
        <button type="submit">Save Movie</button> 
    </form>
</template>

<script setup>
    import { ref, onMounted } from "vue";
    onMounted(() => {
        getCsrfToken();
    });
    
    let csrf_token = ref("");
    let successMessage = ref(""); 
    let errors = ref([]);          
    
    function getCsrfToken() {
        
        fetch('/api/v1/csrf-token')
            .then((response) => response.json())
            .then((data) => { 
                console.log(data);
                csrf_token.value = data.csrf_token;
})
}


    function saveMovie(event) {
    let form_data = new FormData(event.target);
    // let successMessage = ref(""); 
    // let errors = ref([]);    

    // let movieForm = document.getElementById('movieForm');
    // let form_data = new FormData(movieForm); 

    fetch("/api/v1/movies", {
        method: "POST",
        body: form_data,
        headers: {
            'X-CSRFToken': csrf_token.value
        }
    })
    .then(async (response) => {
        const data = await response.json();

        if (response.ok) {
            // SUCCESS
            successMessage.value = data.message ;
            errors.value = []; // clear errors
            event.target.reset(); 
        } else {
            // ERRORS
            successMessage.value = "";
            errors.value = data.errors;
            // errors.value = ["Something went wrong", 'photo field'];

        }
    })
    .catch((err) => {
        console.log(err);
        successMessage.value = "";
        errors.value = ["Server error"];
    });
}

</script>