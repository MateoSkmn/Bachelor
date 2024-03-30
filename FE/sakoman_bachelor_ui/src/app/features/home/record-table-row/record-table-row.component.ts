import { Component, Input, OnDestroy } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { ApiService } from '../../../global/service/api.service';
import { Subscription } from 'rxjs';
import { Router } from '@angular/router';

@Component({
  selector: 'app-record-table-row',
  standalone: true,
  imports: [MatIconModule],
  templateUrl: './record-table-row.component.html',
  styleUrl: './record-table-row.component.scss'
})
export class RecordTableRowComponent implements OnDestroy {

  @Input() fileName: string = "";
  @Input() fileIndex: number = 0;
  @Input() isTrained: boolean = false;

  private deleteSubscription!: Subscription;

  constructor(private apiService: ApiService, private router: Router) {}

  ngOnDestroy(): void {
    if (this.deleteSubscription) {
      this.deleteSubscription.unsubscribe();
    }
  }

  deleteFile(): void {
    this.deleteSubscription = this.apiService.deleteRecord(this.fileName).subscribe({
      next: (response) => {
        console.log(response);
        window.location.reload();
      },
      error: (error) => {
        console.error('Error:', error);
      }
    });
  }
}
