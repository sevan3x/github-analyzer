import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import type { GithubUserResponse } from './models/github-user.model';


@Injectable({
    providedIn: 'root'
})

export class GithubService {

    private apiUrl = 'http://127.0.0.1:8000/api/user';

    constructor(private http: HttpClient) {}

    getUser(username: string) {
        return this.http.get<GithubUserResponse>(this.apiUrl, { params: { username } });
    }

}