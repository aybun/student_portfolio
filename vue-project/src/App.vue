<script setup>
</script>

<template>
  <div id="app">
    <header>
      <div class="flex-shrink-0 p-3 bg-white" style="width: 280px">
      <a
        href="/"
        class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none border-bottom"
      >
        <svg class="bi me-2" width="30" height="24">
          <use xlink:href="#bootstrap" />
        </svg>
        <span class="fs-5 fw-semibold">Profile Management System</span>
      </a>
      <ul class="list-unstyled ps-0">
        <li class="mb-1">
          <button
            class="btn btn-toggle align-items-center rounded collapsed"
            data-bs-toggle="collapse"
            data-bs-target="#home-collapse"
            aria-expanded="true"
          >
            Home
          </button>
          <div class="collapse show" id="home-collapse">
            <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
              <!-- <li><a href="#" class="link-dark rounded">Overview</a></li> -->
            </ul>
          </div>
        </li>
        <li class="mb-1">
          <button
            class="btn btn-toggle align-items-center rounded collapsed"
            data-bs-toggle="collapse"
            data-bs-target="#dashboard-collapse"
            aria-expanded="false"
          >
            Event
          </button>
          <div class="collapse" id="dashboard-collapse">
            <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
              <li><router-link to="/event" class="link-dark rounded" >Event</router-link></li>
              <li><router-link to="/event/event-attended-student" class="link-dark rounded" >Event Attended Student</router-link></li>

            </ul>
          </div>
        </li>
        <li class="mb-1">
          <button
            class="btn btn-toggle align-items-center rounded collapsed"
            data-bs-toggle="collapse"
            data-bs-target="#Profile-collapse"
            aria-expanded="false"
          >
            Profile
          </button>
          <div class="collapse" id="Profile-collapse">
            <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
              <li><router-link to="/skillchart" class="link-dark rounded" >Skill Chart</router-link></li>
              <li><router-link to="/skill" class="link-dark rounded" >Skill</router-link></li>
              <li><router-link to="/skillgroup" class="link-dark rounded" >Skillgroup</router-link></li>
              <li><router-link to="/curriculum" class="link-dark rounded" >Curriculum</router-link></li>
              <!-- <li><a href="#" class="link-dark rounded">Overview</a></li> -->
            </ul>
          </div>
        </li>
        <li class="mb-1">
          <button
            class="btn btn-toggle align-items-center rounded collapsed"
            data-bs-toggle="collapse"
            data-bs-target="#orders-collapse"
            aria-expanded="false"
          >
            Project
          </button>
          <div class="collapse" id="orders-collapse">
            <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
              <li>
                <router-link to="/project" class="link-dark rounded"
                  >Project</router-link
                >
              </li>
              <!-- <li><a href="#" class="link-dark rounded">New</a></li> -->
            </ul>
          </div>
        </li>
        <li class="mb-1">
          <button
            class="btn btn-toggle align-items-center rounded collapsed"
            data-bs-toggle="collapse"
            data-bs-target="#orders-collapse-2"
            aria-expanded="false"
          >
            Award
          </button>
          <div class="collapse" id="orders-collapse-2">
            <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
              <li>
                <router-link to="/award" class="link-dark rounded"
                  >Award</router-link
                >
              </li>
              <!-- <li><a href="#" class="link-dark rounded">New</a></li> -->
            </ul>
          </div>
        </li>
        <li class="border-top my-3"></li>
        <li class="mb-1">
          <button
            class="btn btn-toggle align-items-center rounded collapsed"
            data-bs-toggle="collapse"
            data-bs-target="#account-collapse"
            aria-expanded="false"
          >
            Account
          </button>
          <div class="collapse" id="account-collapse">
            <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
              <li>
                <router-link to="/login-vue" class="link-dark rounded">Login</router-link>

              </li>
              <li><a href="/api/logout" class="link-dark rounded">Sign out</a></li>
            </ul>
          </div>
        </li>
      </ul>
    </div>
    </header>

    <router-view />
  </div>
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
