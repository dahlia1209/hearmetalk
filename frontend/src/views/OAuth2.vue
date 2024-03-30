<template>
    <div class="oauth-view">
        {{ errorMessageRef }}
    </div>
</template>
<script lang="ts" setup>
import { onMounted, ref } from 'vue';

const errorMessageRef = ref("")

onMounted(() => {
    const hash = window.location.hash;
    const params = new URLSearchParams(hash.substring(1));
    const access_token = params.get('access_token');
    const expires_in = params.get('expires_in');

    if (access_token&&expires_in) {
        localStorage.setItem('access_token', access_token);
        localStorage.setItem('expires_in', expires_in);
        window.close()
    } else {
        errorMessageRef.value = "認証失敗"
    }
})

</script>