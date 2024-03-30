import { Component, Input } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { Response } from '../../interfaces/response.interface';
import { ErrorService } from '../../service/error.service';

@Component({
  selector: 'app-notification',
  standalone: true,
  imports: [MatIconModule],
  templateUrl: './notification.component.html',
  styleUrl: './notification.component.scss'
})
export class NotificationComponent {
  @Input({ required: true }) response!: Response;

  constructor(private errorService: ErrorService) {}

  closeNotification(): void {
    this.errorService.triggerError(null);
  }
}
