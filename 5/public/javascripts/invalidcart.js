async function wait_clear_and_redirect() {
    document.cookie = "cart=; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
    await new Promise(r => setTimeout(r, 3000));
    window.location.replace("/");
}

wait_clear_and_redirect();