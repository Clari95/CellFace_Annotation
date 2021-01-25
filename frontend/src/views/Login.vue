<template>
  <v-app>
    <v-content>
      <v-container
        fluid
        fill-height
      >
        <v-layout
          align-center
          justify-center
        >
          <v-flex
            xs12
            sm8
            md4
          >
            <v-card class="elevation-12">
              <v-toolbar
                color="primary"
                dark
                flat
              >
                <v-toolbar-title>Login form</v-toolbar-title>
                <v-spacer></v-spacer>
              </v-toolbar>
              <v-card-text>
                <v-form ref="login-form" v-model="validForm">
                  <v-text-field
                    v-model="username"
                    label="User"
                    name="username"
                    prepend-icon="fa-user"
                    type="text"
                    @keyup.enter="submitLogin"
                    :rules="[ruleIsPresent]"
                    required
                  ></v-text-field>

                  <v-text-field
                    v-model="password"
                    id="password"
                    label="Password"
                    name="password"
                    prepend-icon="fa-lock"
                    type="password"
                    @keyup.enter="submitLogin"
                    :rules="[ruleIsPresent]"
                    required
                  ></v-text-field>

                  <v-btn
                    class="mx-2" color="primary"
                    @click="submitLogin"
                    target="login-form"
                    :disabled="!validForm"
                  >
                    Login
                  </v-btn>
                </v-form>
              </v-card-text>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import { HTTP } from '@/http.common';

export default {

  data: () => ({
    validForm: false,
    username: null,
    password: null,
    ruleIsPresent: v => !!v || 'Field is required',
    ruleValidEmail: v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
  }),

  methods: {
    submitLogin() {
      // console.log(this.$refs['login-form']);
      const formData = new FormData();
      formData.append('username', this.username);
      formData.append('password', this.password);

      HTTP.post('login', formData)
        .then((success) => {
          this.$root.$emit('snackbar', {
            text: success.data.message,
            color: 'success',
          });

          localStorage.setItem('isLoggedIn', true);
          localStorage.setItem('firstName', success.data.first_name);
          localStorage.setItem('lastName', success.data.last_name);

          this.$router.push('/');
        })
        .catch((error) => {
          this.$root.$emit('snackbar', {
            text: `${error.name}: ${error.message}`,
            color: 'error',
          });
        });
    },
  },

};
</script>

<style>

</style>
