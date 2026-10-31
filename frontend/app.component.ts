import { Component } from '@angular/core';
import { GithubService } from './github.service';


@Component({
    selector: 'app-root',
    templateUrl: './app.component.html'
})

export class AppComponent {

    githubUsername = '';
    data: any;
    error = ;

    constructor(private githubService: GithubService) {}

    search() {
    /**
     * TODO: call backend, handle logic
     */
    }

}