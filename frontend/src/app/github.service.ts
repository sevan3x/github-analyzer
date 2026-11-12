import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../environments/environment';
import type { GithubUserResponse } from './models/github-user.model';


@Injectable({
    providedIn: 'root'
})

export class GithubService {

    private readonly apiUrl = `${environment.apiBaseUrl}/api/user`;

    constructor(private http: HttpClient) {}

    getUser(username: string) {
        return this.http.get<GithubUserResponse>(this.apiUrl, { params: { username } });
    }

}
