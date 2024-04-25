import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { ApiService } from '../../../global/service/api.service';
import { ErrorService } from '../../../global/service/error.service';
import { MatIconModule } from '@angular/material/icon';
import { RecordListItem } from '../../../global/interfaces/record-list-item.interface';

@Component({
  selector: 'app-model-table-row',
  standalone: true,
  imports: [MatIconModule],
  templateUrl: './model-table-row.component.html',
  styleUrl: './model-table-row.component.scss'
})
export class ModelTableRowComponent implements OnDestroy {

  @Input() fileName: string = "";
  @Input() fileIndex: number = 0;
  @Input() recordName: string | null = "";
  @Input() recordList: RecordListItem[] = [];

  private deleteSubscription!: Subscription;

  constructor(private apiService: ApiService, private router: Router, private errorService: ErrorService) {}

  ngOnDestroy(): void {
    if (this.deleteSubscription) {
      this.deleteSubscription.unsubscribe();
    }
  }

  deleteFile(): void {
    this.deleteSubscription = this.apiService.deleteModel(this.fileName).subscribe({
      next: (response) => {
        window.location.reload();
      },
      error: (error) => {
        this.errorService.triggerError(error);
      }
    });
  }
}
