import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NotificationComponent } from './global/components/notification/notification.component';
import { Response } from './global/interfaces/response.interface';
import { ErrorService } from './global/service/error.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NotificationComponent],
  templateUrl: './app.component.html'
})
export class AppComponent implements OnInit {
  title = 'sakoman_bachelor_ui';

  response: Response[] = [];

  constructor(private errorService: ErrorService) {}

  ngOnInit() {
    this.errorService.errorEvent.subscribe((error) => {
        // Handles the incoming errors
        this.response = [];
        if(error) {
          this.response.push(error);
        }
    });
  }
}
