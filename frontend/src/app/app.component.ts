import { Component, signal } from '@angular/core';
import type { HttpErrorResponse } from '@angular/common/http';
import { finalize, timeout } from 'rxjs';

import { GithubService } from './github.service';
import type { GithubUserResponse } from './models/github-user.model';


@Component({
    selector: 'app-root',
    standalone: false,
    templateUrl: './app.component.html'
})

export class AppComponent {

    githubUsername = '';

    data = signal<GithubUserResponse | null>(null);
    error = signal('');
    loading = signal(false)

    constructor(private githubService: GithubService) {}

    search() {
        if (this.loading()) {
            return;
        }

        this.data.set(null);
        this.error.set('');

        const username = this.githubUsername.trim();
        const validFormat = /^[A-Za-z0-9]+(-[A-Za-z0-9]+)*$/.test(username);

        if (!validFormat || username.length > 39) {
            this.error.set('Enter a valid GitHub username.');
            return;
        }

        this.loading.set(true);

        this.githubService.getUser(username)
        .pipe(
            timeout(15000),
            finalize(() => this.loading.set(false))
        )
        .subscribe({
            next: (user) => {
                this.data.set(user);
            },
            error: (error: HttpErrorResponse) => {
                const detail = error.error?.detail;

                if (typeof detail === 'string') {
                    this.error.set(detail);
                } else if (error.status === 422) {
                    this.error.set('Enter a valid GitHub username.');
                } else if (error.status === 0) {
                    this.error.set('Cannot connect to the backend.');
                } else {
                    this.error.set('Unable to load the username. Please try again.');
                }
            }
        });
    }

}