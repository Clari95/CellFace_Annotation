/* eslint-disable import/prefer-default-export */
import axios from 'axios';
import { getCookie } from '@/utils.common';

// console.log(`API URL: ${process.env.VUE_APP_API}`);

axios.defaults.headers['X-CSRFToken'] = getCookie('csrftoken');
axios.defaults.withCredentials = true;

const axiosInstance = axios.create({
  baseURL: process.env.VUE_APP_API,
  timeout: 50000,
  headers: {
    // 'Access-Control-Allow-Credentials': true,
    // Authorization: 'Bearer {token}', // we're using session auth, not tokens
    // 'X-CSRFToken': getCookie('csrftoken'),
  },
});

export const HTTP = axiosInstance;
