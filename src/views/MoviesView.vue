<template>
    
    <div class="container mt-4">
    <h2>Movies</h2>

    <!-- <p>{{ movies }}</p> -->

    <!-- <div v-if="movies.length">
        <div v-for="movie in movies" :key="movie.id">
            <h3>{{ movie.title }}</h3>
            <p>{{ movie.description }}</p>
            <img :src="'../uploads/' + movie.poster" width="100" />
        </div>
    </div> -->

    <div class="row">
        <div
        class="col-md-6 mb-3"
        v-for="movie in movies"
        :key="movie.id"
        >
        <div class="card h-100 shadow-sm">
            <div class="row g-0">

             <!-- Poster -->
            <div class="col-4">
                <!-- <img
                :src="'../uploads/' + movie.poster"
                class="img-fluid rounded-start"
                style="height: 100%; object-fit: cover;"
                /> -->
                <img
                :src="'http://localhost:8080/uploads/' + movie.poster"
                class="img-fluid rounded-start"
                style="height: 200px; width: 500px; object-fit: cover;"
                />
            </div>

            <!-- Content -->
            <div class="col-8">
                <div class="card-body">
                <h5 class="card-title">
                    {{ movie.title }}
                </h5>

                <p class="card-text">
                    {{ movie.description }}
                </p>
                </div>
            </div>

            </div>
        </div>
        </div>
    </div>
    </div>  
</template>


<script setup>
    import { ref, onMounted } from "vue";
    
    let movies = ref([]); 

    onMounted(() => {
        // const token = getCsrfToken();
        fetchMovies();  
    });

//     function getCsrfToken() {
//     return document.cookie
//         .split('; ')
//         .find(row => row.startsWith('csrftoken='))
//         ?.split('=')[1];
// }

    function fetchMovies() {
    fetch("http://localhost:8080/api/v1/movies")
        .then(res => res.json())
        .then(data => {
            console.log("MOVIES:", data);
            movies.value = data.movies; 
            // movies.value = data; 
        })
        .catch(err => {
            console.log("Error fetching movies:", err);
        });
}
</script>

